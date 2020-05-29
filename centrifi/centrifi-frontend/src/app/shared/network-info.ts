export interface NetworkInfo {
    wifiName: string,
    meshKey: string,
    aps: Array<APInfo>
}

export interface APInfo{
    apIP: string,
    apMAC: string,
    apType: string
}
    