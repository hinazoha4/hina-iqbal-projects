const mqtt = require('mqtt');
const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

// === Firebase Admin Init ===
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://live-tv-a98f9.firebaseio.com'
});

const db = admin.database();

// === MQTT Broker Config ===
const broker = 'mqtts://b6e0e48a748c4d20971053ddf587142e.s1.eu.hivemq.cloud:8883';
const username = 'espProject';
const password = 'Esp12345678';
const topic = 'quietnight/esp32/data';

// === MQTT Client Setup ===
const client = mqtt.connect(broker, {
  username,
  password,
  rejectUnauthorized: false
});

// === MQTT Events ===
client.on('connect', () => {
  console.log('✅ MQTT connected');
  client.subscribe(topic, (err) => {
    if (err) console.error('❌ MQTT subscribe error:', err.message);
    else console.log('📡 Subscribed to topic:', topic);
  });
});

client.on('message', (topic, message) => {
  try {
    console.log(message.toString())
    const data = JSON.parse(message.toString());
    const timestamp = Date.now();

    // Determine data source (default to "unknown")
    const source = data.source || 'esp32'; // fallback to "esp32" if not provided

    const ref = db.ref(`/data/${source}/${timestamp}`);
    ref.set(data)
      .then(() => console.log(`✅ [${source}] Firebase write successful`, data))
      .catch((err) => console.error('❌ Firebase write failed:', err.message));
  } catch (err) {
    console.error('❌ JSON parse error:', err.message);
  }
});
