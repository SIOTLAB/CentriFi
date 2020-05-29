export interface GetEndDeviceList {
    devices: Device[];
}

export interface Device {
    deviceIP:string;
    deviceName:string;
    deviceMAC:string;
    roamingRestricted: string;
}