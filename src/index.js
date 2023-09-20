const discord = require("discord.js");
require("dotenv").config()

const client = new discord.Client({ intents: [discord.GatewayIntentBits.Guilds] });
const token = process.env.TOKEN;

client.on("ready", () => {
    console.log(`Logged in as ${client.user.username}!`);
});

client.login(token)