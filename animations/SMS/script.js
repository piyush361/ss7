
let tl = gsap.timeline();

tl .to("#mobile-station", { x: 200, duration: 1.2, opacity: 1 })
  .to("#vlr", { x: 400, duration: 1.2, opacity: 1 }, "-=1.2")
  .to("#hlr", { x: -400, duration: 1.2, opacity: 1 }, "-=1.2")
  .to("#bts", { x: -900, duration: 1.2, opacity: 1 }, "-=1.2")
  .to("#smsc", { x: -100, y:-50,duration: 1.2, opacity: 1 }, "-=1.2")
  .to("#msc", { x: 900, duration: 1.2, opacity: 1 }, "-=1.2")
  .to("#rc", {x:-10 , duration:2.2 , opacity:1},"=-1.2");



class MobileStation {
  constructor(number, IMSI) {
      this.number = number;
      this.IMSI = IMSI;
  }

  async sendSMS(recipient, message, baseStation,msc) {
      console.log(`\n[MobileStation] ${this.number} encapsulating message to ${recipient.number}...`);
      let text = `[MobileStation] ${this.number} encapsulating message to ${recipient.number}...`;
      
      console.log(`${this.number} → Sending SMS to ${recipient.number}: "${message}"`);
      text = `[MobileStation] Sending SMS to ${recipient.number}: "${message}"`;
      await animateStep("#mobile-station", text);


      baseStation.forwardSMS(this, recipient, message,msc);
  }

  receiveSMS(sender, message,msc) {
      
      console.log(`[MobileStation] ${this.number} received SMS from ${sender.number}: "${message}"`);
      let text = `[MobileStation] ${this.number} received SMS from ${sender.number}: "${message}..`;
      animateStep("#rc",text);
  }
}

class BaseStation {
  constructor() {
      this.msc = new MobileSwitchingCenter();
  }

  async forwardSMS(sender, recipient, message,msc) {
      console.log(`[Base Station] Received SMS from ${sender.number}, forwarding to MSC...`);
      let text = `[Base Station] Forwarding SMS from ${sender.number} to MSC...`;
      await animateStep("#bts", text);
     // await movePacketTo("#msc");


      this.msc.processSMS(sender, recipient, message,msc);
  }
}

class MobileSwitchingCenter {
  constructor() {
      this.smsc = new ShortMessageServiceCenter();
  }

  async processSMS(sender, recipient, message,msc) {
      console.log(`[MSC] Processing SMS from ${sender.number} to ${recipient.number}...`);
      let text = `[MSC] Processing SMS from ${sender.number} to ${recipient.number}...`;
      //await movePacketTo("#vlr");
      await animateStep("#msc", text);

      if (sender.IMSI in VLR && VLR[sender.IMSI].blacklist) {
          let f = "Checking in the VLR";
          await animateStep("#vlr", f);
          console.log(`[MSC] SMS Blocked: ${sender.number} is blacklisted.`);
          text = `[MSC] SMS Blocked: ${sender.number} is blacklisted.`;
         // await movePacketTo("#msc");
          await animateStep("#msc", text);
          return;
      }

      console.log(`[MSC] Sender ${sender.number} verified! Forwarding to SMSC...`);
      text = `[MSC] Sender ${sender.number} verified! Forwarding to SMSC...`;
    //  await movePacketTo("#smsc");
      await animateStep("#msc", text);

      this.smsc.storeAndForward(sender, recipient, message,msc);
  }

  async deliverSMS(sender, recipient, message) {
      console.log(`[MSC] Delivering SMS from ${sender.number} to ${recipient.number}...`);
      let text = `[MSC] Delivering SMS from ${sender.number} to ${recipient.number}...`;
    //  await movePacketTo("#bts");
      await animateStep("#msc", text);

      recipient.receiveSMS(sender, message);
  }
}

class ShortMessageServiceCenter {
  constructor() {
      //this.msc = new MobileSwitchingCenter();
  }

  async storeAndForward(sender, recipient, message,msc) {
      console.log(`[SMSC] Storing SMS for ${recipient.number}...`);
      let text = `[SMSC] Storing SMS for ${recipient.number}...`;
    //  await movePacketTo("#hlr");
      await animateStep("#smsc", text);

      let f = "Checking in the HLR ...";
      await animateStep("#hlr",f);
      if (!HLR[recipient.number]) {
         
          console.log(`[SMSC] Delivery failed: ${recipient.number} not found in HLR.`);
          text = `[SMSC] Delivery failed: ${recipient.number} not found in HLR.`;
         // await movePacketTo("#smsc");
          await animateStep("#smsc", text);
          return;
      }

      console.log(`[SMSC] Located ${recipient.number} in HLR. Forwarding to MSC...`);
      text = `[SMSC] Located ${recipient.number} in HLR. Forwarding to MSC...`;
     // await movePacketTo("#msc");
      await animateStep("#smsc", text);
      
      msc.deliverSMS(sender, recipient, message);
  }
}



const VLR = {
    "123456789012345": { available: 1, blacklist: true, sms_service: 1, balance: 50 }
};

const HLR = {
    "+919876543210": { available: 1, blacklist: false, sms_service: 1, balance: 100 },
    "67890":{available:1 , blacklist:false , sms_service:1 , balance:100}
};



// GSAP animation integration
async function animateStep(element,text) {
    return new Promise(resolve => {
        document.getElementById("ct").innerText=text;
        document.getElementById("tt").innerText=text
        if (element == "#mobile-station") {
          gsap.to("#text-container", {  y: -900, duration: 1.2, opacity: 1 , onComplete: () => {
            gsap.to("#text-container", { 
                opacity: 0, 
                duration: 1.2, 
                delay:1.2,
                onComplete: () => {
                  gsap.set("#text-container", { y: 0, opacity: 0 }); // Reset position
                  resolve(); // Proceed to next step
              } // Only resolve after fading out
            });
        }});
      } 
      else if (element == "#bts") {
        gsap.to("#text-container", { x:520, y: -1050, duration: 1.2, opacity: 1 ,delay:1.2, onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); // Reset position
                resolve(); // Proceed to next step
            } // Only resolve after fading out
          });
      }});
      } else if (element == "#msc") {
        gsap.to("#text-container", { x:820, y: -870, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); // Reset position
                resolve(); // Proceed to next step
            } // Only resolve after fading out
          });
      }});
    }
       else if (element == "#vlr") {
        gsap.to("#lookup", { x:420, y: 0, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#lookup", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#lookup", { y: 0, opacity: 0 }); // Reset position
                resolve(); // Proceed to next step
            } // Only resolve after fading out
          });
      }});
      } else if (element == "#hlr") {
        gsap.to("#lookup", { x:220, y: 0, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#lookup", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#lookup", { y: 0, opacity: 0 }); // Reset position
                resolve(); // Proceed to next step
            } // Only resolve after fading out
          });
      }});
      } else if (element == "#smsc") {
        gsap.to("#text-container", { x:1120, y: -950, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); // Reset position
                resolve(); // Proceed to next step
            } // Only resolve after fading out
          });
      }});
      }
      else if (element == "#rc") {
        gsap.to("#text-container", { x:1020, y: -1270, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); // Reset position
                resolve(); // Proceed to next step
            } // Only resolve after fading out
          });
      }});
      }

      
    });
}






document.getElementById("start-btn").addEventListener("click", function() {
  document.getElementById("message-popup").style.display = "block";
});

document.getElementById("send-message").addEventListener("click", function() {
  let message = document.getElementById("message-input").value.trim();
  if (message) {
      document.getElementById("message-popup").style.display = "none";
      startSimulation(message);
  } else {
      alert("Please enter a message!");
  }
});

function startSimulation(message) {
  let sender = new MobileStation("12345", "123456");
  let recipient = new MobileStation("67890", "I678");
  let baseStation = new BaseStation();
  let msc = new MobileSwitchingCenter();
  sender.sendSMS(recipient, message, baseStation,msc);
}



