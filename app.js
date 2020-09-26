const hap = require("hap-nodejs");

const Accessory = hap.Accessory;
const Characteristic = hap.Characteristic;
const CharacteristicEventTypes = hap.CharacteristicEventTypes;
const Service = hap.Service;

const accessoryUUID = hap.uuid.generate("com.wjwickham.sabotage-box");// Using reverse-DNS style identifiers better ensures uniqueness.
const accessory = new Accessory("Electrical Sabotage Box", accessoryUUID);

/* The HomeKit accessory exposes a single switch. 
 * This switch is used to trigger a HomeKit automation or scene when
 * the box triggers a “sabotage“. The automation/scene is what actually
 * turns off lights and other accessories.
 */
const switchService = new Service.Lightbulb("Sabotage Trigger");
let switchState = false;

const onCharacteristic = switchService.getCharacteristic(Characteristic.On);

onCharacteristic.on(CharacteristicEventTypes.GET, callback => {
  console.log("HomeKit asked for the current state of the sabotage trigger.");
  callback(undefined, switchState);
});

onCharacteristic.on(CharacteristicEventTypes.SET, (value, callback) => {
  console.log("HomeKit is changing the state of the sabotage trigger to: " + value);
  switchState = value;
  callback();
});

accesory.addService(switchService);

accessory.publish({
  username: "17:51:07:F4:BC:8A",
  pincode: "678-90-876",
  port: 47129,
  category: hap.Categories.SWITCH, // value here defines the symbol shown in the pairing screen
});