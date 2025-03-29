
async function animateStep(ele, text) {
    return new Promise(resolve=>{
        document.getElementById("ct").innerText=text;
        document.getElementById("tt").innerText=text;
        if (ele == "#s") {
          gsap.to("#text-container", {  y: -425,x: -160, duration: 1.2, opacity: 1 , onComplete: () => {
            gsap.to("#text-container", { 
                opacity: 0, 
                duration: 1.2, 
                delay:1.2,
                onComplete: () => {
                  gsap.set("#text-container", { y: 0, opacity: 0 }); 
                  resolve(); 
              } 
            });
        }});
      }
      if (ele == "#bts1") {
        gsap.to("#text-container", {  y: -685,x: -345, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); 
                resolve(); 
            } 
          });
      }});
    }
    if (ele == "#bsc1") {
        gsap.to("#text-container", {  y: -585,x: 195, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); 
                resolve(); 
            } 
          });
      }});
    }
    if (ele == "#msc1") {
        gsap.to("#text-container", {  y: -985,x: -100, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); 
                resolve(); 
            } 
          });
      }});
    }
    if (ele == "#hlr") {
        gsap.to("#lookup", {  x: 395, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#lookup", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#lookup", { y: 0, opacity: 0 }); 
                resolve(); 
            } 
          });
      }});
    }
    if (ele == "#gmsc") {
        gsap.to("#text-container", {  y: -1185,x: 100, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); 
                resolve(); 
            } 
          });
      }});
    }

    if (ele == "#msc2") {
        gsap.to("#text-container", {  y: -985,x: 900, duration: 1.2, opacity: 1 , onComplete: () => {
          gsap.to("#text-container", { 
              opacity: 0, 
              duration: 1.2, 
              delay:1.2,
              onComplete: () => {
                gsap.set("#text-container", { y: 0, opacity: 0 }); 
                resolve(); 
            } 
          });
      }});
    }
    
    



        
    })
}

document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.createElement("button");
    startButton.textContent = "Start Call";
    startButton.style.padding = "5px 10px";
    startButton.style.fontSize = "12px";
    startButton.style.cursor = "pointer";
    startButton.style.width = "200px";
    startButton.style.height = "100px";
    document.body.appendChild(startButton);

    startButton.addEventListener("click", () => {
        const logElement = document.createElement("pre");
        document.body.appendChild(logElement);
        caller.callInitiated(recipient, logElement).then(() => {
            setTimeout(() => {
                msc1.endCall(caller, recipient, logElement);
            }, 3000);
        });
    });
});

class MobileStation {
    constructor(number, IMSI, netid, msc, bts) {
        this.number = number;
        this.IMSI = IMSI;
        this.netid = netid;
        this.msc = msc;
        this.bts = bts;
        this.signalStrength = Math.floor(Math.random() * 51) + 50;
    }

    async callInitiated(recipient) {
        await animateStep("#s", `[MS] Initiating Call Setup for ${recipient.number}`);
        await this.sleep(1000);
        await this.bts.forwardCall(this, recipient);
    }

    async checkSignalStrength() {
        if (this.signalStrength < 60) {
            let newBts = this.bts.bsc.getStrongerBts();
            if (newBts) {
                await animateStep("#s", `[MS] Weak signal detected. Initiating handover to BTS-${newBts.id}`);
                this.bts = newBts;
            }
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

class BaseStation {
    constructor(id, bsc) {
        this.id = id;
        this.bsc = bsc;
    }

    async forwardCall(caller, recipient) {
        await animateStep("#bts1", `[BTS-${this.id}] Forwarding call request to BSC-${this.bsc.id}`);
        await caller.sleep(1000);
        await caller.checkSignalStrength();
        await this.bsc.processCall(caller, recipient);
    }
}

class BSC {
    constructor(id, msc) {
        this.id = id;
        this.msc = msc;
        this.btsList = [];
    }

    addBts(bts) {
        this.btsList.push(bts);
    }

    async processCall(caller, recipient) {
        await animateStep(`#bsc${this.id}`, `[BSC-${this.id}] Allocating channel...`);
        await caller.sleep(1000);
        await animateStep(`#bsc${this.id}`, `[BSC-${this.id}] Channel ${Math.floor(Math.random() * 151)} allocated`);
        await caller.sleep(1000);
        await this.msc.processCall(caller, recipient);
    }
}

class MSC {
    constructor(id, gmsc = null) {
        this.id = id;
        this.gmsc = gmsc;
    }

    async processCall(caller, recipient) {
        await animateStep(`#msc${this.id}`, `[MSC-${this.id}] IAM: Call request for ${recipient.number}`);
        await caller.sleep(1000);
        if (caller.netid === recipient.netid) {
            await this.connectCall(caller, recipient);
        } else {
            await animateStep(`#msc${this.id}`, `[MSC-${this.id}] Forwarding call to GMSC for inter-network routing`);
            await caller.sleep(1000);
            await this.gmsc.routeCall(caller, recipient);
        }
    }

    async connectCall(caller, recipient) {
        await animateStep(`#msc${this.id}`, `[MSC-${this.id}] ACM: Querying HLR for location of ${recipient.number}`);
        await caller.sleep(1300);
        await animateStep(`#msc${this.id}`, `[MSC-${this.id}] ANM: Call connected to ${recipient.number}`);
    }
}

class GMSC {
    constructor() {
        this.networks = {};
    }

    addNetwork(netid, msc) {
        this.networks[netid] = msc;
    }

    async routeCall(caller, recipient) {
        if (this.networks[recipient.netid]) {
            let targetMsc = this.networks[recipient.netid];
            await animateStep("#gmsc", `[GMSC] Routing call to MSC-${targetMsc.id}`);
            await caller.sleep(1000);
            await targetMsc.connectCall(caller, recipient);
        } else {
            await animateStep("#gmsc", `[GMSC] No route available. Call failed.`);
        }
    }
}

const gmsc = new GMSC();
const msc1 = new MSC(1, gmsc);
const msc2 = new MSC(2, gmsc);
gmsc.addNetwork(1, msc1);
gmsc.addNetwork(2, msc2);

const bsc1 = new BSC(1, msc1);
const bsc2 = new BSC(2, msc2);

const bts1 = new BaseStation(1, bsc1);
const bts2 = new BaseStation(2, bsc2);

bsc1.addBts(bts1);
bsc2.addBts(bts2);

const caller = new MobileStation("9876543210", "IMSI-12345", 1, msc1, bts1);
const recipient = new MobileStation("9123456780", "IMSI-67890", 2, msc2, bts2);