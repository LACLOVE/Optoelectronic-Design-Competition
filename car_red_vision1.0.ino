int M11=3;
int M12=5;
int M21=10;
int M22=11;
int led=13;
void setup()
{
  Serial.begin(9600);
  pinMode(led,OUTPUT);
  pinMode(M11,OUTPUT);analogWrite(M11,0);
  pinMode(M12,OUTPUT);analogWrite(M12,0);
  pinMode(M21,OUTPUT);analogWrite(M21,0);
  pinMode(M22,OUTPUT);analogWrite(M22,0);

}

void loop()
{
    int num=0;

    int a=0; 

while(Serial.available()>0)

    {

        num=num*10;

    a=Serial.read()-'0';

        num=num+a;

        delay(5);
    }
    Serial.println(num);
    if(300<=num<=340)
    { 
        SetMotor(255,255);
    }
    else if(num>340)
    {
        SetMotor(-120,255);
    }
    else if(0<num<300)
    {
        SetMotor(255,-120);
    }
    else if(num==0)
    {
        SetMotor(0,0);
    }
    while(Serial.available()==0){};
}
void SetMotor(float v1,float v2)
{
  if (v1>255){v1=255;analogWrite(M11,0);analogWrite(M12,v1);}
  else if (v1>0) {analogWrite(M11,0);analogWrite(M12,v1);}
  else if (v1>-255) {analogWrite(M12,0);analogWrite(M11,-v1);}
  else  {v1=-255;analogWrite(M12,0);analogWrite(M11,-v1);}
  
  if (v2>255){v2=255;analogWrite(M21,0);analogWrite(M22,v2);}
  else if (v2>0) {analogWrite(M21,0);analogWrite(M22,v2);}
  else if (v2>-255) {analogWrite(M22,0);analogWrite(M21,-v2);}
  else {v2=-255;analogWrite(M22,0);analogWrite(M21,-v2);}  
}




