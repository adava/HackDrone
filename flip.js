var arDrone = require('ar-drone');
var client  = arDrone.createClient();

client.takeoff();

client
/*  .after(2000, function() {
    this.up(1);
  })
*/
  .after(4000, function() {
    this.animate('flipLeft', 14);
  })
  .after(6000, function() {
    this.animate('flipRight', 14);
  })

  .after(6000, function() {
    this.animate('flipLeft', 14);
  })

  .after(4000, function() {
    this.land();
  });
