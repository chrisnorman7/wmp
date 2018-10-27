// MUD proxy stuff.

let soc = null
const connectForm = document.getElementById("connectForm")
const hostname = document.getElementById("hostname")
const port = document.getElementById("port")
const main = document.getElementById("main")
const disconnect = document.getElementById("disconnect")
const output = document.getElementById("output")
const entryForm = document.getElementById("entryForm")
const entry = document.getElementById("entry")

main.hidden = true

function write_message(message) {
    p = document.createElement("p")
    p.innerText = message
    output.appendChild(p)
    window.scrollTo(0,document.body.scrollHeight)
}

connectForm.onsubmit = (e) => {
    e.preventDefault()
    if (!hostname.value) {
        alert("You must enter a hostname.")
        hostname.focus()
    } else {
        soc = new WebSocket('ws://{{ host }}:{{ port }}')
        soc.onclose = (e) => {
            soc = null
            connectForm.hidden = false
            write_message(`*** Socket closed [${e.code}]: ${e.reason || "None"} ***`)
        }
        soc.onerror = () => write_message("*** Socket error. ***")
        soc.onmessage = (e) => write_message(e.data)
        soc.onopen = () => {
            soc.send(hostname.value)
            soc.send(port.value)
            connectForm.hidden = true
            main.hidden = false
            write_message('*** Connecting. ***')
        }
    }
}

entryForm.onsubmit = (e) => {
    e.preventDefault()
    soc.send(entry.value)
    entry.value = ""
}

window.addEventListener(
    "beforeunload", (e) => {
        if (soc) {
            e.returnValue = "You are currently connected. Are you sure you want to disconnect?"
            return e.returnValue
        }
    }
)

disconnect.onclick = () => {
    if (soc) {
        if (confirm("Are you sure you want to disconnect?")) {
            soc.close(1000, "User clicked the Disconnect button.")
        }
    } else {
        alert("You are not connected.")
    }
}
