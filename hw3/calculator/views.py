from django.shortcuts import render
# Create your views here.

def calculator(request):
    context = {}
    newValue = 0
    
    if not 'newValue' in request.POST:
        newValue = 0
    else:
        newValue = int(request.POST['newValue'])
    
    if not 'preValue' in request.POST:
        preValue = 0
        print("preValue not in post")
    else:
        preValue = int(request.POST['preValue'])
        print("preValue in POST")
        print(preValue)
    
    if not 'preOp' in request.POST:
        preOp = u'+'
    else:
        preOp = request.POST['preOp']
    
    if not 'lastClickIsDigit' in request.POST:
        lastClickIsDigit = "False"
    else:
        lastClickIsDigit = request.POST['lastClickIsDigit']

    
    if 'number' in request.POST:
        number = request.POST['number']
        if len(number) == 0:
        	context['preValue'] = preValue
        	context['preOp'] = preOp
        	context['result'] = "Invalid"
        	context['lastClickIsDigit'] = "False"
        else:
        	newValue = int(newValue)*10+int(number)
	        context['newValue'] = newValue
	        context['preValue'] = preValue
	        context['preOp'] = preOp
	        context['result'] = newValue
	        context['lastClickIsDigit'] = "True"
        
    
    if 'op' in request.POST:
        result = 0
        op = request.POST['op']
        if len(op) == 0:
        	context['preValue'] = 0
        	context['newValue'] = 0
        	context['preOp'] = u'+'
        	context['result'] = "Invalid"
        	context['lastClickIsDigit'] = "False"
        elif lastClickIsDigit == "True":
            if preOp == u'+':
                result = preValue + newValue
            elif preOp == u'-':
                result = preValue - newValue
            elif preOp == u'*':
                result = preValue * newValue
            elif preOp ==  u'/':
                if newValue == 0:
                    context['preValue'] = 0
                    context['newValue'] = 0
                    context['preOp'] = u'+'
                    context['result'] = "ERROR!"
                    context['lastClickIsDigit'] = "False"
                    return render(request, 'calculator/calculator.html', context)
                else:
                    result = int(preValue/newValue)
            elif preOp == u'=':
                result = newValue
            else:
                return
            
            context['result'] = result
            context['preValue'] = result
            context['preOp'] = op
            context['newValue'] = 0
            context['lastClickIsDigit'] = "False"
        else:
            context['newValue'] = newValue
            context['preValue'] = preValue
            context['preOp'] = op
            context['result'] = preValue
            context['lastClickIsDigit'] = "False"
    return render(request, 'calculator/calculator.html', context)

