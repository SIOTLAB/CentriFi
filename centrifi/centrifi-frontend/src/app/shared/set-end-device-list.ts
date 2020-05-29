export interface SetEndDeviceList {
    devices: Device[];
}

export interface Device {
    deviceMAC:string;
    roamingRestricted: string;
}