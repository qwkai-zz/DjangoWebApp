var newValue=0;
var preValue=0;
var preOp="+";
var lastClickIsDigit=false;

function clickDigit(digit){
  //console.log(digit);
  //console.log(newValue);
  newValue = parseInt(newValue)*10+parseInt(digit);
  //console.log(newValue);
  document.getElementById("result").value = newValue;
  lastClickIsDigit=true;
}

function clickOp(operator){
  //console.log(operator);
  var result=0;
  if(lastClickIsDigit){
    if(preOp=="+"){
      result = preValue+newValue;
    }else if(preOp=="-"){
      result = preValue-newValue;
    }else if(preOp=="*"){
      result = preValue*newValue;
    }else if(preOp=="/"){
      // console.log(preValue);
      // console.log(newValue);
      if(newValue==0){
        alert("Sorry, you cannot divide by zero!");
        preValue=0;
        newValue=0;
        preOp="+";
        document.getElementById("result").value=0;
        return;
      }else{
        result = parseInt(preValue/newValue);
      }
    }else if(preOp=="="){
      result = newValue;
    }else{
      return;
    }
    document.getElementById("result").value=result;
    preValue = result;
    preOp = operator;
    newValue = 0;
    lastClickIsDigit=false;
  }else{
    preOp=operator;
    lastClickIsDigit=false;
  }


}
