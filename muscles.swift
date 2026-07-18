import Foundation

// SWIFT: The Muscles that talk to the hardware
let processInfo = ProcessInfo.processInfo
let uptime = processInfo.systemUptime
let cores = processInfo.activeProcessorCount
let hostName = processInfo.hostName

// Calculate hours and minutes from raw uptime seconds
let hours = Int(uptime) / 3600
let minutes = (Int(uptime) % 3600) / 60

print("⚡ SWIFT HARDWARE LINK ACTIVE")
print("   • HOST IDENTITY: \(hostName)")
print("   • CPU CORES: \(cores) (Neural Engine Ready)")
print("   • SYSTEM UPTIME: \(hours) hours, \(minutes) minutes")
print("   • STATUS: MAX PERFORMANCE")
