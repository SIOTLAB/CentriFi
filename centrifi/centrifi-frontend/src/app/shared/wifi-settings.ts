export interface WifiSettings {
    networkName: string;
    password: string;
    security: string;
    aps: APSettingInfo[];
}

export interface APSettingInfo{
    apIP: string;
    channel: string;
}
