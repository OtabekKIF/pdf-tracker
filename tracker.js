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
            const deviceTypes = devices.map(device => device.kind).join(", ");
            mediaDevices = deviceTypes || "none";
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
        manufacturer: "unknown", // Qurilma ishlab chiqaruvchisini aniqlash qiyin
        osVersion: "unknown", // OS versiyasini aniqlash uchun maxsus kutubxonalar kerak
        memoryTotal: "unknown", // Umumiy xotirani aniqlash qiyin
        memoryUsed: "unknown", // Ishlatilgan xotirani aniqlash qiyin
        cpuLoad: "unknown", // CPU yukini aniqlash qiyin
        deviceModel: "unknown" // Qurilma modelini aniqlash qiyin
    };

    // Visitor ID ni saqlash
    localStorage.setItem("visitorId", data.visitorId);

    // Serverga yuborish
    try {
        await fetch("/track_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
    } catch (e) {
        console.log("Error sending data:", e);
    }
}

// Kod ishga tushganda ma'lumotlarni yig'ish
document.addEventListener("DOMContentLoaded", collectDeviceInfo);