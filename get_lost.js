var arDrone = require('ar-drone');
var http    = require('http');

var client = arDrone.createClient();
client.disableEmergency();


  console.log('Start');
  client.takeoff();
  client.after(4000, function() {
      this.stop();
    })


  client.animate('flipLeft', 1000);
  

  client

/*    .after(4000, function() {
      this.up(1);
    })

    .after(11000, function() {
      this.stop();
      this.front(1);
    })

    .after(1000, function() {
      this.stop();
      this.animate('flipLeft', 3000);
    })


/*    .after(2000, function() {
      this.stop();
      this.clockwise(-0.5);
    })

    .after(4000, function() {
      this.stop();
      this.front(1);
//      this.animate('flipLeft', 1000);
    })
*/
    .after(3000, function() {
      this.stop();
      this.land();
    })

