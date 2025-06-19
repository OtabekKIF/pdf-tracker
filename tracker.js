async function collectDeviceInfo() {
    let batteryInfo = "unknown";
    try {
        if (navigator.getBattery) {
            const battery = await navigator.getBattery();
            batteryInfo = `Level: ${battery.level * 100}%, Charging: ${battery.charging}`;
        }
    } catch (e) {
        console.log("Battery info error:", e);
    }

    const mediaDevices = "unknown";
    try {
        if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
            const devices = await navigator.mediaDevices.enumerateDevices();
            mediaDevices = devices.map(device => device.kind).join(", ") || "none";
        }
    } catch (e) {
        console.log("Media devices error:", e);
    }

    const data = {
        visitorId: localStorage.getItem("visitorId") || Math.random().toString(36).substring(2),
        screen: `${window.screen.width}x${window.screen.height}`,
        colorDepth: window.screen.colorDepth || "unknown",
        language: navigator.language || "unknown",
        platform: navigator.platform || "unknown",
        userAgent: navigator.userAgent || "unknown",
        cpu: navigator.hardwareConcurrency ? `${navigator.hardwareConcurrency} cores` : "unknown",
        ram: navigator.deviceMemory ? `${navigator.deviceMemory} GB` : "unknown",
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "unknown",
        localTime: new Date().toLocaleString() || "unknown",
        doNotTrack: navigator.doNotTrack || "unknown",
        battery: batteryInfo,
        media: mediaDevices,
        networkType: navigator.connection ? navigator.connection.effectiveType : "unknown",
        deviceType: navigator.connection ? navigator.connection.type : "unknown",
        manufacturer: "unknown",
        osVersion: "unknown",
        memoryTotal: "unknown",
        memoryUsed: "unknown",
        cpuLoad: "unknown",
        deviceModel: "unknown"
    };

    localStorage.setItem("visitorId", data.visitorId);

    try {
        await fetch("https://pdf-tracker-t4fc.onrender.com/track_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
    } catch (e) {
        console.log("Error sending data:", e);
    }
}

document.addEventListener("DOMContentLoaded", collectDeviceInfo);
