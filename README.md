# pharmacy-directory
This django application helps in finding relative drugs by searching for the drugs with same compositions.

<b> Working: </b><br /><br />
Basically, this app helps you find the related drugs when you search for one drug. There are two sections, one for the pharmaceuticals,
who can enter the drugs and the related compositions. And another one is for general people who can then search for the drugs.

As soon as anyone places a query for a drug, the program checks for its availability in the database. If found one then it looks up for
its compositions. After the compositions are collected, it goes for all the drugs in the database and then matches compositions. After that 
all the drugs with similar compositions are sorted based on the highest similarity in compositions with queried durg
which is determined by a simple scoring mechanism. 

And in this way user gets the related drugs on the basis of composition.


<i>authentication is only for someone who wants to get into this app totally. Otherwise you can scrap working parts.</i>


<b> Authentication: </b><br /> <br  />
It has a very complicated authentication system for the pharmaceuticals, just because pharma. business is very critical and motivating if anyone
goes for money. 

Pharmaceuticals needs to signup first with credentials like mobile number and email address. As soon as they signup they
will be sent an authentication link to email address and a integer code to mobile number. The authentication link will redirect to another 
page where the pharma. will be asked to enter the code sent to mobile number. Then only, the pharma will receive a file which 
should be used every time while placing entries for the drugs. Actually the file is nothing but encrypted id which is used for entering into
dataase.


The app can be a bit messy, because it was created on a 36 hour hackathon. 

I'd be super happy if anyone want's to adopt anything from this thing. If you wanna know anything about this whole mumble jumble, just mail 
me on getsurajjha@gmai.com.

Thanks for reading this mess. I would have fallen distracted halfway.
