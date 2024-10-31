import re, openpyxl, subprocess, os, inquirer

def correcao_mac(mac):
   letras_num = 'abcdefghijklmnopqrstuvwxyz0123456789'
   var = mac.lower()
   palavra = ''


   for letra in var:
       if letra in letras_num:
           palavra += letra
   return palavra

def write_text(path, text):
    with open(path, 'w') as f:
        f.write(text)


def replace_pat(filename, pattern, replacement):
    with open(filename, 'r') as file:
        text = file.read()
        text = re.sub(pattern, replacement, text)

    with open(filename, 'w') as file:
        file.write(text)


def shell(command):
    process = subprocess.Popen(command ,shell=True ,stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')

    return stdout


def create_model(path_file, model):
    text = re.sub('%ASTER%', ip_asterisk, model)
    text = re.sub('%PASS%', pass_asterisk, text)
    text = re.sub('%WEB_PASS%', pass_web, text)

    with open(path_file, 'w') as f:
        f.write(text)

# Paths
path_planilha = '/srv/tftp/'
path_dest_macfiles = '/srv/tftp/'
path_dest_models = '/srv/tftp/'

# Declaração de variáveis
ip_asterisk = ''
quant_arquivos = 0
vlans_dic = {}
continue_ask = ''
lista_modelos = [r'cp-?3905', r'cp-?7821', r'cp-?7942', r'cp-?8845', r'cp-?8865', r'cp-?9845', \
                    r'gxp-?1615', r'gxp-?1625', r'gxp-?2170', 't22p']

# Configuração dos telefones
gxp1625_model = '''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Grandstream XML Provisioning Configuration -->
<gs_provision version="1">
<config version="1">
<!-- Sip Server -->
<!-- P47>%ASTER%</P47 -->

<!-- Authenticate Password -->
<P34>%PASS%</P34>

<!-- Account Display -->
<P2480>1</P2480>

<!-- Preferred Vocoder 1 - G.722 -->
<P57>9</P57>

<!-- Preferred Vocoder 2 - PCMA -->
<P58>8</P58>

<!-- NTP Server
<P30></P30> -->

<!-- Time Zone (-3) -->
<P64>BRST+3</P64>

<!-- Formato da data - dd-mm-yyyy -->
<P102>2</P102>

<!-- Formato da hora - 0-24h -->
<P122>1</P122>

<!-- Voice Vlan -->
<P51></P51>

<!-- Configuracao via TFTP -->
<P212>0</P212>

<!-- Caminho da configuracao no TFTP
<P237></P237> -->

<!-- Linguagem -->
<P1362>pt</P1362>

<!-- Mostrar o User ID na tela -->
<P2380>1</P2380>

<!-- Admin password for web interface -->
<P2>%WEB_PASS%</P2>

<!-- Dial Plan -->
<P290>{ ** | **x+ | x+ | #x+ | #*x+ }</P290>

<!-- Ringtone -->
<P104>3</P104>
</config>
</gs_provision>
'''
gxp2170_model = '''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Grandstream XML Provisioning Configuration -->
<gs_provision version="1">
<config version="1">
<!-- Forma de configuracao - TFTP -->
<P212>0</P212>

<!-- Servidor de configuracao
<P237></P237> -->

<!-- SIP Server -->
<!-- P47>%ASTER%</P47 -->

<!-- Password -->
<P34>%PASS%</P34>

<!-- Preferencia 1 de Codec - G.722 -->
<P57>9</P57>

<!-- Preferencia 2 de Codec - PCMA -->
<P58>8</P58>

<!-- NTP Server
<P30></P30> -->

<!-- Formato da data - dd-mm-yyyy -->
<P102>2</P102>

<!-- Mostrar data na barra superior -->
<P8387>1</P8387>

<!-- Formato da hora - 0-24h -->
<P122>1</P122>

<!-- Time Zone (-3) -->
<P64>BRST+3</P64>

<!-- Descanso de Tela -->
<P2918>0</P2918>
<!-- Desligar o bluetooth -->
<P2910>0</P2910>

<!-- Wallpaper download -->
<P2916>1</P2916>

<!-- Caminho do wallpaper -->
<P2917></P2917>

<!-- Voice Vlan -->
<P51></P51>

<!-- Linguagem -->
<P1362>pt</P1362>

<!-- Admin password for web interface -->
<P2>%WEB_PASS%</P2>

<!-- Dial Plan -->
<P290>{ ** | **x+ | x+ | #x+ | #*x+ }</P290>

<!-- City Code Auto -->
<P1405>0</P1405>

<!-- City Code -->
<P1377>Rio de Janeiro, RJ, Brazil</P1377>

<!-- Update Interval -->
<P1378>60</P1378>

<!-- Unidade Temp -->
<P1379>C</P1379> -->

</config>
</gs_provision>
'''
cp_3905 = '''<device>
<deviceProtocol>SIP</deviceProtocol>
<sshUserId>cisco</sshUserId>
<sshPassword>cisco</sshPassword>
<devicePool>
<dateTimeSetting>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>SA Eastern Standard Time</timeZone>
<ntps>
<ntp>
    <!-- SERVIDOR DE DATA e HORA - não altere  -->
    <name>%NTP%</name>
    <ntpMode>Unicast</ntpMode>
</ntp>
</ntps>
</dateTimeSetting>
<callManagerGroup>
<members>
<member priority="0">
    <callManager>
        <ports>
            <ethernetPhonePort>2000</ethernetPhonePort>
            <sipPort>5060</sipPort>
            <securedSipPort>5061</securedSipPort>
        </ports>

        <!-- IP ou FQDN (host) do SERVIDOR REGISTRO SIP (seu Asterisk, por exemplo) -->
        <processNodeName>$asterisk</processNodeName>

    </callManager>
</member>
</members>
</callManagerGroup>
</devicePool>
<sipProfile>
<sipProxies>
<backupProxy></backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy></emergencyProxy>
<emergencyProxyPort></emergencyProxyPort>
<outboundProxy></outboundProxy>
<outboundProxyPort></outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>x-serviceuri-cfwdall</callForwardURI>
<callPickupURI>x-cisco-serviceuri-pickup</callPickupURI>
<callPickupListURI>x-cisco-serviceuri-opickup</callPickupListURI>

<callPickupGroupURI>x-cisco-serviceuri-gpickup</callPickupGroupURI>
<meetMeServiceURI>x-cisco-serviceuri-meetme</meetMeServiceURI>

<abbreviatedDialURI>x-cisco-serviceuri-abbrdial</abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>2</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>2</callerIdBlocking>
<dndControl>0</dndControl>
<remoteCcEnable>true</remoteCcEnable>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>false</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>false</transferOnhookEnabled>
<enableVad>false</enableVad>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
<kpml>3</kpml>

<!-- Seu nome com até 13 caracteres, sem espaços -->
<phoneLabel>$nome</phoneLabel>

<stutterMsgWaiting>1</stutterMsgWaiting>
<callStats>false</callStats>

<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<sipLines>
<line button="1">
<featureID>9</featureID>

<!-- IP ou FQDN (host) do SERVIDOR REGISTRO SIP (seu Asterisk, por exemplo) -->
<proxy>%ASTER%</proxy>
<port>5060</port>

<!-- Usuário SIP ou ramal -->
<featureLabel>%RAMAL%</featureLabel>

<!-- Usuário SIP ou ramal -->
<name>%RAMAL%</name>

<!-- Usuário SIP ou ramal -->
<displayName>%NOME%</displayName>

<!-- Usuário SIP ou ramal -->
<authName>%RAMAL%</authName>

<!-- Usuário SIP ou ramal -->
<contact>%RAMAL%</contact>

<!-- SENHA da conta SIP -->
<authPassword>%PASS%</authPassword>

<autoAnswer>
    <autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messagesNumber>*97</messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>

<forwardCallInfoDisplay>
    <callerName>true</callerName>
    <callerNumber>false</callerNumber>
    <redirectedNumber>false</redirectedNumber>
    <dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
</line>
</sipLines>

<!-- Parâmetros da conta SIP -->
<voipControlPort>5060</voipControlPort>
<startMediaPort>10000</startMediaPort>
<stopMediaPort>20000</stopMediaPort>

<dscpForAudio>184</dscpForAudio>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>dialplan.xml</dialTemplate>
<softKeyFile></softKeyFile>
</sipProfile>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>

<!-- Versao do Firmware para auto upgrade (se estiver na mesma pasta TFTP) -->
<loadInformation>CP3905.9-4-1SR2-2</loadInformation>

<vendorConfig>
<disableSpeaker>false</disableSpeaker>
<disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
<pcPort>0</pcPort>
<settingsAccess>1</settingsAccess>
<garp>0</garp>
<voiceVlanAccess>0</voiceVlanAccess>
<videoCapability>0</videoCapability>
<autoSelectLineEnable>0</autoSelectLineEnable>
<webAccess>1</webAccess>
<daysDisplayNotActive>1,2,3,4,5,6,7</daysDisplayNotActive>
<displayOnTime>00:00</displayOnTime>
<displayOnDuration>00:00</displayOnDuration>
<displayIdleTimeout>00:00</displayIdleTimeout>
<spanToPCPort>1</spanToPCPort>
<loggingDisplay>1</loggingDisplay>
<loadServer></loadServer>
</vendorConfig>
<userLocale>
<name></name>
<uid></uid>
<langCode>Brazil</langCode>
<version>1.0.0.0-1</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>Brazil</name>
<uid></uid>
<version>1.0.0.0-1</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<servicesURL></servicesURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>2</transportLayerProtocol>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
</device>
'''
cp_7821 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
<sshUserId>cisco</sshUserId>
<sshPassword>cisco</sshPassword>
<sshAccess>0</sshAccess>
<sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>j9-tzdata.jar</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
<ntps>
    <ntp>
        <name>%NTP%</name>
    <ntpMode>Unicast</ntpMode>
    </ntp>
</ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<address></address>
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>0</callerIdBlocking>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>false</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
    <authName>%RAMAL%</authName>
    <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber>%RAMAL%</messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact>%RAMAL%</contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="2" lineIndex="2">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
    <authName></authName>
    <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>



</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>sip78xx.12-5-1SR1-4</loadInformation>
<vendorConfig>
<defaultWallpaperFile></defaultWallpaperFile>
<disableSpeaker>false</disableSpeaker>
<disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
<enableMuteFeature>false</enableMuteFeature>
<enableGroupListen>true</enableGroupListen>
<holdResumeKey>1</holdResumeKey>
<recentsSoftKey>1</recentsSoftKey>
<dfBit>1</dfBit>
<pcPort>0</pcPort>
<spanToPCPort>1</spanToPCPort>
<garp>0</garp>
<rtcp>1</rtcp>
<videoRtcp>1</videoRtcp>
<voiceVlanAccess>0</voiceVlanAccess>
<videoCapability>1</videoCapability>
<hideVideoByDefault>0</hideVideoByDefault>
<separateMute>0</separateMute>
<ciscoCamera>1</ciscoCamera>
<usb1>1</usb1>
<usb2>1</usb2>
<usbClasses>0,1,2</usbClasses>
<sdio>1</sdio>
<wifi>1</wifi>
<bluetooth>1</bluetooth>
<bluetoothProfile>0,1</bluetoothProfile>
<btpbap>0</btpbap>
<bthfu>0</bthfu>
<ehookEnable>0</ehookEnable>
<autoSelectLineEnable>1</autoSelectLineEnable>
<autoCallSelect>1</autoCallSelect>
<incomingCallToastTimer>10</incomingCallToastTimer>
<dialToneFromReleaseKey>0</dialToneFromReleaseKey>
<joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
<minimumRingVolume></minimumRingVolume>
<simplifiedNewCall>0</simplifiedNewCall>
<actionableAlert>0</actionableAlert>
<showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
<kemOneColumn>0</kemOneColumn>
<lineMode>0</lineMode>
<allCallsOnPrimary>0</allCallsOnPrimary>
<softKeyControl>0</softKeyControl>
<settingsAccess>1</settingsAccess>
<webProtocol>0</webProtocol>
<webAccess>0</webAccess>
<webAdmin>1</webAdmin>
<adminPassword></adminPassword>
<sshAccess>0</sshAccess>
<detectCMConnectionFailure>0</detectCMConnectionFailure>
<g722CodecSupport>1</g722CodecSupport>
<handsetWidebandEnable>2</handsetWidebandEnable>
<headsetWidebandEnable>2</headsetWidebandEnable>
<headsetWidebandUIControl>1</headsetWidebandUIControl>
<handsetWidebandUIControl>1</handsetWidebandUIControl>
<daysDisplayNotActive>1,7</daysDisplayNotActive>
<displayOnTime>08:00</displayOnTime>
<displayOnDuration>10:00</displayOnDuration>
<displayIdleTimeout>00:10</displayIdleTimeout>
<displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
<displayRefreshRate>0</displayRefreshRate>
<daysBacklightNotActive>1,7</daysBacklightNotActive>
<backlightOnTime>08:00</backlightOnTime>
<backlightOnDuration>10:00</backlightOnDuration>
<backlightIdleTimeout>00:10</backlightIdleTimeout>
<backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
<recordingTone>0</recordingTone>
<recordingToneLocalVolume>100</recordingToneLocalVolume>
<recordingToneRemoteVolume>50</recordingToneRemoteVolume>
<recordingToneDuration></recordingToneDuration>
<moreKeyReversionTimer>5</moreKeyReversionTimer>
<peerFirmwareSharing>0</peerFirmwareSharing>
<loadServer></loadServer>
<problemReportUploadURL></problemReportUploadURL>
<enableCdpSwPort>1</enableCdpSwPort>
<enableCdpPcPort>0</enableCdpPcPort>
<enableLldpSwPort>1</enableLldpSwPort>
<enableLldpPcPort>0</enableLldpPcPort>
<cdpEnable>true</cdpEnable>
<outOfRangeAlert>0</outOfRangeAlert>
<scanningMode>2</scanningMode>
<applicationURL></applicationURL>
<appButtonTimer>0</appButtonTimer>
<appButtonPriority>0</appButtonPriority>
<specialNumbers></specialNumbers>
<sendKeyAction>0</sendKeyAction>
<powerOffWhenCharging>0</powerOffWhenCharging>
<homeScreen>0</homeScreen>
<accessContacts>1</accessContacts>
<accessFavorites>1</accessFavorites>
<accessVoicemail>1</accessVoicemail>
<accessApps>1</accessApps>
</vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL>http://10.52.66.23:5000/contactsMenu?company=FAB_RCAER&amp;group=CCA_RJ</directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>2</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName>%ASTER%</processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url><directoryURL></directoryURL></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
'''
cp_7942 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
<sshUserId>cisco</sshUserId>
<sshPassword>cisco</sshPassword>
<sshAccess>0</sshAccess>
<sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>tzupdaterTropico.jar</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
<ntps>
    <ntp>
        <name>%NTP%</name>
    <ntpMode>Unicast</ntpMode>
    </ntp>
</ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<!--address>VSS.tropiconet.com</address-->
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>0</callerIdBlocking>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>true</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
    <authName>%RAMAL%</authName>
    <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="2" lineIndex="2">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
    <authName></authName>
    <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>4</busyTrigger>
</line>



</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>SIP42.9-4-2SR3-1S</loadInformation>
<vendorConfig>
<defaultWallpaperFile></defaultWallpaperFile>
<disableSpeaker>false</disableSpeaker>
<disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
<enableMuteFeature>false</enableMuteFeature>
<enableGroupListen>true</enableGroupListen>
<holdResumeKey>1</holdResumeKey>
<recentsSoftKey>1</recentsSoftKey>
<dfBit>1</dfBit>
<pcPort>0</pcPort>
<spanToPCPort>1</spanToPCPort>
<garp>0</garp>
<rtcp>1</rtcp>
<videoRtcp>1</videoRtcp>
<voiceVlanAccess>0</voiceVlanAccess>
<videoCapability>1</videoCapability>
<hideVideoByDefault>0</hideVideoByDefault>
<separateMute>0</separateMute>
<ciscoCamera>1</ciscoCamera>
<usb1>1</usb1>
<usb2>1</usb2>
<usbClasses>0,1,2</usbClasses>
<sdio>1</sdio>
<wifi>1</wifi>
<bluetooth>1</bluetooth>
<bluetoothProfile>0,1</bluetoothProfile>
<btpbap>0</btpbap>
<bthfu>0</bthfu>
<ehookEnable>0</ehookEnable>
<autoSelectLineEnable>1</autoSelectLineEnable>
<autoCallSelect>1</autoCallSelect>
<incomingCallToastTimer>10</incomingCallToastTimer>
<dialToneFromReleaseKey>0</dialToneFromReleaseKey>
<joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
<minimumRingVolume></minimumRingVolume>
<simplifiedNewCall>0</simplifiedNewCall>
<actionableAlert>0</actionableAlert>
<showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
<kemOneColumn>0</kemOneColumn>
<lineMode>0</lineMode>
<allCallsOnPrimary>0</allCallsOnPrimary>
<softKeyControl>0</softKeyControl>
<settingsAccess>1</settingsAccess>
<webProtocol>0</webProtocol>
<webAccess>0</webAccess>
<webAdmin>1</webAdmin>
<adminPassword></adminPassword>
<sshAccess>0</sshAccess>
<detectCMConnectionFailure>0</detectCMConnectionFailure>
<g722CodecSupport>1</g722CodecSupport>
<handsetWidebandEnable>2</handsetWidebandEnable>
<headsetWidebandEnable>2</headsetWidebandEnable>
<headsetWidebandUIControl>1</headsetWidebandUIControl>
<handsetWidebandUIControl>1</handsetWidebandUIControl>
<daysDisplayNotActive>1,7</daysDisplayNotActive>
<displayOnTime>08:00</displayOnTime>
<displayOnDuration>10:00</displayOnDuration>
<displayIdleTimeout>00:10</displayIdleTimeout>
<displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
<displayRefreshRate>0</displayRefreshRate>
<daysBacklightNotActive>1,7</daysBacklightNotActive>
<backlightOnTime>08:00</backlightOnTime>
<backlightOnDuration>10:00</backlightOnDuration>
<backlightIdleTimeout>00:10</backlightIdleTimeout>
<backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
<recordingTone>0</recordingTone>
<recordingToneLocalVolume>100</recordingToneLocalVolume>
<recordingToneRemoteVolume>50</recordingToneRemoteVolume>
<recordingToneDuration></recordingToneDuration>
<moreKeyReversionTimer>5</moreKeyReversionTimer>
<peerFirmwareSharing>0</peerFirmwareSharing>
<loadServer></loadServer>
<problemReportUploadURL></problemReportUploadURL>
<enableCdpSwPort>1</enableCdpSwPort>
<enableCdpPcPort>0</enableCdpPcPort>
<enableLldpSwPort>1</enableLldpSwPort>
<enableLldpPcPort>0</enableLldpPcPort>
<cdpEnable>true</cdpEnable>
<outOfRangeAlert>0</outOfRangeAlert>
<scanningMode>2</scanningMode>
<applicationURL></applicationURL>
<appButtonTimer>0</appButtonTimer>
<appButtonPriority>0</appButtonPriority>
<specialNumbers></specialNumbers>
<sendKeyAction>0</sendKeyAction>
<powerOffWhenCharging>0</powerOffWhenCharging>
<homeScreen>0</homeScreen>
<accessContacts>1</accessContacts>
<accessFavorites>1</accessFavorites>
<accessVoicemail>1</accessVoicemail>
<accessApps>1</accessApps>
</vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>1</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName></processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="1" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="1" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="1" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url><directoryURL></directoryURL></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
'''
cp_8845 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
<sshUserId>cisco</sshUserId>
<sshPassword>cisco</sshPassword>
<sshAccess>0</sshAccess>
<sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>j9-tzdata.jar</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>SA Eastern Standard Time</timeZone>
    <ntps>
        <ntp>
            <name>%NTP%</name>
        <ntpMode>Unicast</ntpMode>
        </ntp>
    </ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member priority="0">
<callManager>
<name>ASTERISK</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1/>
<port1>2000</port1>
<ipAddr2/>
<port2>2000</port2>
<ipAddr3/>
<port3>2000</port3>
<sipIpAddr1/>
<sipPort1>5060</sipPort1>
<sipIpAddr2/>
<sipPort2>5060</sipPort2>
<sipIpAddr3/>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<address></address>
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>7</callForwardURI>
<callPickupURI>x-cisco-serviceuri-pickup</callPickupURI>
<callPickupListURI/>
<callPickupGroupURI>x-cisco-serviceuri-gpickup</callPickupGroupURI>
<meetMeServiceURI/>
<abbreviatedDialURI/>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>0</callerIdBlocking>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>false</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel/>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
        <authName>%RAMAL%</authName>
        <authPassword>%PASS</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<!--

<line button="2" lineIndex="2">
<featureID>9</featureID>
<featureLabel/>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
        <authName></authName>
        <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

-->

<!--

<line button="3" lineIndex="3">
<featureID>9</featureID>
<featureLabel/>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
        <authName></authName>
        <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

-->


</sipLines>
<externalNumberMask/>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>dialplan.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword/>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>sip8845_65.12-5-1SR2-2</loadInformation>

<vendorConfig>
<defaultWallpaperFile/>
<disableSpeaker>false</disableSpeaker>
<disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
<enableMuteFeature>false</enableMuteFeature>
<enableGroupListen>true</enableGroupListen>
<holdResumeKey>1</holdResumeKey>
<recentsSoftKey>1</recentsSoftKey>
<dfBit>1</dfBit>
<pcPort>0</pcPort>
<spanToPCPort>1</spanToPCPort>
<garp>0</garp>
<rtcp>1</rtcp>
<videoRtcp>1</videoRtcp>
<voiceVlanAccess>0</voiceVlanAccess>
<videoCapability>1</videoCapability>
<hideVideoByDefault>0</hideVideoByDefault>
<separateMute>0</separateMute>
<ciscoCamera>1</ciscoCamera>
<usb1>1</usb1>
<usb2>1</usb2>
<usbClasses>0,1,2</usbClasses>
<sdio>1</sdio>
<wifi>1</wifi>
<bluetooth>1</bluetooth>
<bluetoothProfile>0,1</bluetoothProfile>
<btpbap>0</btpbap>
<bthfu>0</bthfu>
<ehookEnable>0</ehookEnable>
<autoSelectLineEnable>1</autoSelectLineEnable>
<autoCallSelect>1</autoCallSelect>
<incomingCallToastTimer>10</incomingCallToastTimer>
<dialToneFromReleaseKey>0</dialToneFromReleaseKey>
<joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
<minimumRingVolume/>
<simplifiedNewCall>0</simplifiedNewCall>
<actionableAlert>0</actionableAlert>
<showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
<kemOneColumn>0</kemOneColumn>
<lineMode>0</lineMode>
<allCallsOnPrimary>0</allCallsOnPrimary>
<softKeyControl>0</softKeyControl>
<settingsAccess>1</settingsAccess>
<webProtocol>0</webProtocol>
<webAccess>0</webAccess>
<webAdmin>1</webAdmin>
<adminPassword/>
<sshAccess>0</sshAccess>
<detectCMConnectionFailure>0</detectCMConnectionFailure>
<g722CodecSupport>1</g722CodecSupport>
<handsetWidebandEnable>2</handsetWidebandEnable>
<headsetWidebandEnable>2</headsetWidebandEnable>
<headsetWidebandUIControl>1</headsetWidebandUIControl>
<handsetWidebandUIControl>1</handsetWidebandUIControl>
<daysDisplayNotActive>1,7</daysDisplayNotActive>
<displayOnTime>08:00</displayOnTime>
<displayOnDuration>10:00</displayOnDuration>
<displayIdleTimeout>00:10</displayIdleTimeout>
<displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
<displayRefreshRate>0</displayRefreshRate>
<daysBacklightNotActive>1,7</daysBacklightNotActive>
<backlightOnTime>08:00</backlightOnTime>
<backlightOnDuration>10:00</backlightOnDuration>
<backlightIdleTimeout>00:10</backlightIdleTimeout>
<backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
<recordingTone>0</recordingTone>
<recordingToneLocalVolume>100</recordingToneLocalVolume>
<recordingToneRemoteVolume>50</recordingToneRemoteVolume>
<recordingToneDuration/>
<moreKeyReversionTimer>5</moreKeyReversionTimer>
<peerFirmwareSharing>0</peerFirmwareSharing>
<loadServer/>
<problemReportUploadURL/>
<enableCdpSwPort>1</enableCdpSwPort>
<enableCdpPcPort>0</enableCdpPcPort>
<enableLldpSwPort>1</enableLldpSwPort>
<enableLldpPcPort>0</enableLldpPcPort>
<cdpEnable>true</cdpEnable>
<outOfRangeAlert>0</outOfRangeAlert>
<scanningMode>2</scanningMode>
<applicationURL/>
<appButtonTimer>0</appButtonTimer>
<appButtonPriority>0</appButtonPriority>
<specialNumbers/>
<sendKeyAction>0</sendKeyAction>
<powerOffWhenCharging>0</powerOffWhenCharging>
<homeScreen>0</homeScreen>
<accessContacts>1</accessContacts>
<accessFavorites>1</accessFavorites>
<accessVoicemail>1</accessVoicemail>
<accessApps>1</accessApps>
</vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name></name>
<uid>1</uid>
<langCode>pt</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale/>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<idleTimeout>0</idleTimeout>
<authenticationURL/>
<directoryURL></directoryURL>
<idleURL/>
<informationURL/>
<messagesURL/>
<proxyServerURL/>
<servicesURL/>
<secureAuthenticationURL/>
<secureDirectoryURL/>
<secureIdleURL/>
<secureInformationURL/>
<secureMessagesURL/>
<secureServicesURL/>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>2</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName>$asterisk</processNodeName>
</capf>
</capfList>
<certHash/>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn/>
<dtmfdn/>
<ivrdn/>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices useHTTPS="true">
<provisioning>2</provisioning>
<phoneService type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor/>
<version/>
</phoneService>
<phoneService type="0" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor/>
<version/>
</phoneService>
<phoneService type="0" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor/>
<version/>
</phoneService>
<phoneService type="0" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor/>
<version/>
</phoneService>
<phoneService type="0" category="0">
<name>Personal Directory</name>
<url/>
<vendor/>
<version/>
</phoneService>
<phoneService type="0" category="0">
<name>Corporate Directory</name>
<url><directoryURL></directoryURL></url>
<vendor/>
<version/>
</phoneService>
</phoneServices>


</device>
'''
cp_8865 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
<sshUserId>cisco</sshUserId>
<sshPassword>cisco</sshPassword>
<sshAccess>0</sshAccess>
<sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>j9-tzdata.jar</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
<ntps>
    <ntp>
        <name>%NTP%</name>
    <ntpMode>Unicast</ntpMode>
    </ntp>
</ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<address></address>
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<callerIdBlocking>0</callerIdBlocking>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>false</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
    <authName>%RAMAL%</authName>
    <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber>%RAMAL%</messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact>%RAMAL%</contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="2" lineIndex="2">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
    <authName></authName>
    <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>

<line  button="3" lineIndex="3">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name></name>
    <authName></authName>
    <authPassword></authPassword>
<displayName></displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber></messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact></contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>1</busyTrigger>
</line>




</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>sip8845_65.12-5-1SR1-4</loadInformation>

<vendorConfig>
<defaultWallpaperFile></defaultWallpaperFile>
<disableSpeaker>false</disableSpeaker>
<disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
<enableMuteFeature>false</enableMuteFeature>
<enableGroupListen>true</enableGroupListen>
<holdResumeKey>1</holdResumeKey>
<recentsSoftKey>1</recentsSoftKey>
<dfBit>1</dfBit>
<pcPort>0</pcPort>
<spanToPCPort>1</spanToPCPort>
<garp>0</garp>
<rtcp>1</rtcp>
<videoRtcp>1</videoRtcp>
<voiceVlanAccess>0</voiceVlanAccess>
<videoCapability>1</videoCapability>
<hideVideoByDefault>0</hideVideoByDefault>
<separateMute>0</separateMute>
<ciscoCamera>1</ciscoCamera>
<usb1>1</usb1>
<usb2>1</usb2>
<usbClasses>0,1,2</usbClasses>
<sdio>1</sdio>
<wifi>1</wifi>
<bluetooth>1</bluetooth>
<bluetoothProfile>0,1</bluetoothProfile>
<btpbap>0</btpbap>
<bthfu>0</bthfu>
<ehookEnable>0</ehookEnable>
<autoSelectLineEnable>1</autoSelectLineEnable>
<autoCallSelect>1</autoCallSelect>
<incomingCallToastTimer>10</incomingCallToastTimer>
<dialToneFromReleaseKey>0</dialToneFromReleaseKey>
<joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
<minimumRingVolume></minimumRingVolume>
<simplifiedNewCall>0</simplifiedNewCall>
<actionableAlert>0</actionableAlert>
<showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
<kemOneColumn>0</kemOneColumn>
<lineMode>0</lineMode>
<allCallsOnPrimary>0</allCallsOnPrimary>
<softKeyControl>0</softKeyControl>
<settingsAccess>1</settingsAccess>
<webProtocol>0</webProtocol>
<webAccess>0</webAccess>
<webAdmin>1</webAdmin>
<adminPassword></adminPassword>
<sshAccess>0</sshAccess>
<detectCMConnectionFailure>0</detectCMConnectionFailure>
<g722CodecSupport>1</g722CodecSupport>
<handsetWidebandEnable>2</handsetWidebandEnable>
<headsetWidebandEnable>2</headsetWidebandEnable>
<headsetWidebandUIControl>1</headsetWidebandUIControl>
<handsetWidebandUIControl>1</handsetWidebandUIControl>
<daysDisplayNotActive>1,7</daysDisplayNotActive>
<displayOnTime>08:00</displayOnTime>
<displayOnDuration>10:00</displayOnDuration>
<displayIdleTimeout>00:10</displayIdleTimeout>
<displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
<displayRefreshRate>0</displayRefreshRate>
<daysBacklightNotActive>1,7</daysBacklightNotActive>
<backlightOnTime>08:00</backlightOnTime>
<backlightOnDuration>10:00</backlightOnDuration>
<backlightIdleTimeout>00:10</backlightIdleTimeout>
<backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
<recordingTone>0</recordingTone>
<recordingToneLocalVolume>100</recordingToneLocalVolume>
<recordingToneRemoteVolume>50</recordingToneRemoteVolume>
<recordingToneDuration></recordingToneDuration>
<moreKeyReversionTimer>5</moreKeyReversionTimer>
<peerFirmwareSharing>0</peerFirmwareSharing>
<loadServer></loadServer>
<problemReportUploadURL></problemReportUploadURL>
<enableCdpSwPort>1</enableCdpSwPort>
<enableCdpPcPort>0</enableCdpPcPort>
<enableLldpSwPort>1</enableLldpSwPort>
<enableLldpPcPort>0</enableLldpPcPort>
<cdpEnable>true</cdpEnable>
<outOfRangeAlert>0</outOfRangeAlert>
<scanningMode>2</scanningMode>
<applicationURL></applicationURL>
<appButtonTimer>0</appButtonTimer>
<appButtonPriority>0</appButtonPriority>
<specialNumbers></specialNumbers>
<sendKeyAction>0</sendKeyAction>
<powerOffWhenCharging>0</powerOffWhenCharging>
<homeScreen>0</homeScreen>
<accessContacts>1</accessContacts>
<accessFavorites>1</accessFavorites>
<accessVoicemail>1</accessVoicemail>
<accessApps>1</accessApps>
</vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>2</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName>%ASTER%</processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService type="0" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url><directoryURL></directoryURL></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
'''
cp_9845 = '''<?xml version="1.0" encoding="UTF-8"?>
<device>
<fullConfig>true</fullConfig>
<deviceProtocol>SIP</deviceProtocol>
<sshUserId>cisco</sshUserId>
<sshPassword>cisco</sshPassword>
<sshAccess>0</sshAccess>
<sshPort>22</sshPort>
<ipAddressMode>0</ipAddressMode>
<allowAutoConfig>true</allowAutoConfig>
<ipPreferenceModeControl>0</ipPreferenceModeControl>
<tzdata>
<tzolsonversion>tzdata2019c</tzolsonversion>
<tzupdater>TzDataCSV.csv</tzupdater>
</tzdata>
<devicePool>
<revertPriority>0</revertPriority>
<name>Default</name>
<dateTimeSetting>
<name>CMLocal</name>
<dateTemplate>D/M/Y</dateTemplate>
<timeZone>E. South America Standard/Daylight Time</timeZone>
<olsonTimeZone>America/Sao_Paulo</olsonTimeZone>
<ntps>
    <ntp>
        <name>%NTP%</name>
    <ntpMode>Unicast</ntpMode>
    </ntp>
</ntps>
</dateTimeSetting>
<callManagerGroup>
<name>Default</name>
<tftpDefault>true</tftpDefault>
<members>
<member  priority="0">
<callManager>
<name>VSSPBX</name>
<description>PBXSIP</description>
<ports>
<ethernetPhonePort>2000</ethernetPhonePort>
<sipPort>5060</sipPort>
<securedSipPort>5061</securedSipPort>
<mgcpPorts>
<listen>2427</listen>
<keepAlive>2428</keepAlive>
</mgcpPorts>
</ports>
<processNodeName>%ASTER%</processNodeName>
</callManager>
</member>
</members>
</callManagerGroup>
<srstInfo  uuid="{cd241e11-4a58-4d3d-9661-f06c912a18a3}">
<name>Disable</name>
<srstOption>Disable</srstOption>
<userModifiable>false</userModifiable>
<ipAddr1></ipAddr1>
<port1>2000</port1>
<ipAddr2></ipAddr2>
<port2>2000</port2>
<ipAddr3></ipAddr3>
<port3>2000</port3>
<sipIpAddr1></sipIpAddr1>
<sipPort1>5060</sipPort1>
<sipIpAddr2></sipIpAddr2>
<sipPort2>5060</sipPort2>
<sipIpAddr3></sipIpAddr3>
<sipPort3>5060</sipPort3>
<isSecure>false</isSecure>
</srstInfo>
<mlppDomainId>-1</mlppDomainId>
<mlppIndicationStatus>Default</mlppIndicationStatus>
<preemption>Default</preemption>
<connectionMonitorDuration>120</connectionMonitorDuration>
</devicePool>
<TVS>
<members>
<member  priority="0">
<port>2445</port>
<!--servidor para validar arquivos de configuração criptografados-->
<!--address>VSS.tropiconet.com</address-->
</member>
</members>
</TVS>
<sipProfile>
<sipProxies>
<backupProxy>USECALLMANAGER</backupProxy>
<backupProxyPort>5060</backupProxyPort>
<emergencyProxy>USECALLMANAGER</emergencyProxy>
<emergencyProxyPort>5060</emergencyProxyPort>
<outboundProxy>USECALLMANAGER</outboundProxy>
<outboundProxyPort>5060</outboundProxyPort>
<registerWithProxy>true</registerWithProxy>
</sipProxies>
<sipCallFeatures>
<cnfJoinEnabled>true</cnfJoinEnabled>
<callForwardURI>*21*</callForwardURI>
<callPickupURI>#20</callPickupURI>
<callPickupListURI></callPickupListURI>
<callPickupGroupURI>#10</callPickupGroupURI>
<meetMeServiceURI></meetMeServiceURI>
<abbreviatedDialURI></abbreviatedDialURI>
<rfc2543Hold>false</rfc2543Hold>
<callHoldRingback>1</callHoldRingback>
<localCfwdEnable>true</localCfwdEnable>
<semiAttendedTransfer>true</semiAttendedTransfer>
<anonymousCallBlock>2</anonymousCallBlock>
<remoteCcEnable>true</remoteCcEnable>
<retainForwardInformation>false</retainForwardInformation>
</sipCallFeatures>
<sipStack>
<sipInviteRetx>6</sipInviteRetx>
<sipRetx>10</sipRetx>
<timerInviteExpires>180</timerInviteExpires>
<timerRegisterExpires>3600</timerRegisterExpires>
<timerRegisterDelta>5</timerRegisterDelta>
<timerKeepAliveExpires>3600</timerKeepAliveExpires>
<timerSubscribeExpires>3600</timerSubscribeExpires>
<timerSubscribeDelta>5</timerSubscribeDelta>
<timerT1>500</timerT1>
<timerT2>4000</timerT2>
<maxRedirects>70</maxRedirects>
<remotePartyID>true</remotePartyID>
<userInfo>None</userInfo>
</sipStack>
<autoAnswerTimer>1</autoAnswerTimer>
<autoAnswerAltBehavior>false</autoAnswerAltBehavior>
<autoAnswerOverride>true</autoAnswerOverride>
<transferOnhookEnabled>true</transferOnhookEnabled>
<enableVad>false</enableVad>
<preferredCodec>g711alaw</preferredCodec>
<dtmfAvtPayload>101</dtmfAvtPayload>
<dtmfDbLevel>3</dtmfDbLevel>
<dtmfOutofBand>avt</dtmfOutofBand>
<kpml>3</kpml>
<phoneLabel>%RAMAL%</phoneLabel>
<stutterMsgWaiting>2</stutterMsgWaiting>
<callStats>true</callStats>
<offhookToFirstDigitTimer>15000</offhookToFirstDigitTimer>
<T302Timer>15000</T302Timer>
<silentPeriodBetweenCallWaitingBursts>10</silentPeriodBetweenCallWaitingBursts>
<disableLocalSpeedDialConfig>false</disableLocalSpeedDialConfig>
<poundEndOfDial>false</poundEndOfDial>
<startMediaPort>16384</startMediaPort>
<stopMediaPort>32766</stopMediaPort>
<sipLines>
<line  button="1" lineIndex="1">
<featureID>9</featureID>
<featureLabel></featureLabel>
<proxy>USECALLMANAGER</proxy>
<port>5060</port>
<name>%RAMAL%</name>
    <authName>%RAMAL%</authName>
    <authPassword>%PASS%</authPassword>
<displayName>%NOME%</displayName>
<autoAnswer>
<autoAnswerEnabled>2</autoAnswerEnabled>
</autoAnswer>
<callWaiting>3</callWaiting>
<sharedLine>false</sharedLine>
<messageWaitingLampPolicy>1</messageWaitingLampPolicy>
<messageWaitingAMWI>1</messageWaitingAMWI>
<messagesNumber>2121017921</messagesNumber>
<ringSettingIdle>4</ringSettingIdle>
<ringSettingActive>5</ringSettingActive>
<contact>2121017921</contact>
<forwardCallInfoDisplay>
<callerName>true</callerName>
<callerNumber>true</callerNumber>
<redirectedNumber>true</redirectedNumber>
<dialedNumber>true</dialedNumber>
</forwardCallInfoDisplay>
<maxNumCalls>4</maxNumCalls>
<busyTrigger>4</busyTrigger>
</line>

<line  button="2" >
<featureID>2</featureID>
<featureLabel>Rapida00</featureLabel>
<speedDialNumber>0#</speedDialNumber>
</line>

<line  button="3">
<featureID>2</featureID>
<featureLabel>Rapida01</featureLabel>
<speedDialNumber>1#</speedDialNumber>
</line>
<line  button="4">
<featureID>2</featureID>
<featureLabel>Rapida02</featureLabel>
<speedDialNumber>2#</speedDialNumber>
</line>

</sipLines>
<externalNumberMask></externalNumberMask>
<voipControlPort>5060</voipControlPort>
<dscpForAudio>184</dscpForAudio>
<dscpVideo>136</dscpVideo>
<dscpForTelepresence>128</dscpForTelepresence>
<ringSettingBusyStationPolicy>0</ringSettingBusyStationPolicy>
<dialTemplate>DialplanCISCO.xml</dialTemplate>
<softKeyFile>SofteyCISCO.xml</softKeyFile>
<alwaysUsePrimeLine>false</alwaysUsePrimeLine>
<alwaysUsePrimeLineVoiceMail>false</alwaysUsePrimeLineVoiceMail>
</sipProfile>
<MissedCallLoggingOption>10</MissedCallLoggingOption>
<commonProfile>
<phonePassword></phonePassword>
<backgroundImageAccess>true</backgroundImageAccess>
<callLogBlfEnabled>2</callLogBlfEnabled>
</commonProfile>
<loadInformation>SIP894x.9-4-2SR3-1</loadInformation>
<vendorConfig>
<defaultWallpaperFile></defaultWallpaperFile>
<disableSpeaker>false</disableSpeaker>
<disableSpeakerAndHeadset>false</disableSpeakerAndHeadset>
<enableMuteFeature>false</enableMuteFeature>
<enableGroupListen>true</enableGroupListen>
<holdResumeKey>1</holdResumeKey>
<recentsSoftKey>1</recentsSoftKey>
<dfBit>1</dfBit>
<pcPort>0</pcPort>
<spanToPCPort>1</spanToPCPort>
<garp>0</garp>
<rtcp>1</rtcp>
<videoRtcp>1</videoRtcp>
<voiceVlanAccess>0</voiceVlanAccess>
<videoCapability>1</videoCapability>
<hideVideoByDefault>0</hideVideoByDefault>
<separateMute>0</separateMute>
<ciscoCamera>1</ciscoCamera>
<usb1>1</usb1>
<usb2>1</usb2>
<usbClasses>0,1,2</usbClasses>
<sdio>1</sdio>
<wifi>1</wifi>
<bluetooth>1</bluetooth>
<bluetoothProfile>0,1</bluetoothProfile>
<btpbap>0</btpbap>
<bthfu>0</bthfu>
<ehookEnable>0</ehookEnable>
<autoSelectLineEnable>1</autoSelectLineEnable>
<autoCallSelect>1</autoCallSelect>
<incomingCallToastTimer>10</incomingCallToastTimer>
<dialToneFromReleaseKey>0</dialToneFromReleaseKey>
<joinAndDirectTransferPolicy>0</joinAndDirectTransferPolicy>
<minimumRingVolume></minimumRingVolume>
<simplifiedNewCall>0</simplifiedNewCall>
<actionableAlert>0</actionableAlert>
<showCallHistoryForSelectedLine>0</showCallHistoryForSelectedLine>
<kemOneColumn>0</kemOneColumn>
<lineMode>0</lineMode>
<allCallsOnPrimary>0</allCallsOnPrimary>
<softKeyControl>0</softKeyControl>
<settingsAccess>1</settingsAccess>
<webProtocol>0</webProtocol>
<webAccess>0</webAccess>
<webAdmin>1</webAdmin>
<adminPassword></adminPassword>
<sshAccess>0</sshAccess>
<detectCMConnectionFailure>0</detectCMConnectionFailure>
<g722CodecSupport>1</g722CodecSupport>
<handsetWidebandEnable>2</handsetWidebandEnable>
<headsetWidebandEnable>2</headsetWidebandEnable>
<headsetWidebandUIControl>1</headsetWidebandUIControl>
<handsetWidebandUIControl>1</handsetWidebandUIControl>
<daysDisplayNotActive>1,7</daysDisplayNotActive>
<displayOnTime>08:00</displayOnTime>
<displayOnDuration>10:00</displayOnDuration>
<displayIdleTimeout>00:10</displayIdleTimeout>
<displayOnWhenIncomingCall>1</displayOnWhenIncomingCall>
<displayRefreshRate>0</displayRefreshRate>
<daysBacklightNotActive>1,7</daysBacklightNotActive>
<backlightOnTime>08:00</backlightOnTime>
<backlightOnDuration>10:00</backlightOnDuration>
<backlightIdleTimeout>00:10</backlightIdleTimeout>
<backlightOnWhenIncomingCall>1</backlightOnWhenIncomingCall>
<recordingTone>0</recordingTone>
<recordingToneLocalVolume>100</recordingToneLocalVolume>
<recordingToneRemoteVolume>50</recordingToneRemoteVolume>
<recordingToneDuration></recordingToneDuration>
<moreKeyReversionTimer>5</moreKeyReversionTimer>
<peerFirmwareSharing>0</peerFirmwareSharing>
<loadServer></loadServer>
<problemReportUploadURL></problemReportUploadURL>
<enableCdpSwPort>1</enableCdpSwPort>
<enableCdpPcPort>0</enableCdpPcPort>
<enableLldpSwPort>1</enableLldpSwPort>
<enableLldpPcPort>0</enableLldpPcPort>
<cdpEnable>true</cdpEnable>
<outOfRangeAlert>0</outOfRangeAlert>
<scanningMode>2</scanningMode>
<applicationURL></applicationURL>
<appButtonTimer>0</appButtonTimer>
<appButtonPriority>0</appButtonPriority>
<specialNumbers></specialNumbers>
<sendKeyAction>0</sendKeyAction>
<powerOffWhenCharging>0</powerOffWhenCharging>
<homeScreen>0</homeScreen>
<accessContacts>1</accessContacts>
<accessFavorites>1</accessFavorites>
<accessVoicemail>1</accessVoicemail>
<accessApps>1</accessApps>
</vendorConfig>




<commonConfig>
</commonConfig>
<enterpriseConfig>
</enterpriseConfig>
<versionStamp>1373534010-5adf0f73-390c-4a23-b02e-d2f045a13945</versionStamp>
<userLocale>
<name>portuguese_brazil</name>
<uid>1</uid>
<langCode>pt_BR</langCode>
<version>8.5.0.0(1)</version>
<winCharSet>iso-8859-1</winCharSet>
</userLocale>
<networkLocale></networkLocale>
<networkLocaleInfo>
<name>brazil</name>
<uid>64</uid>
<version>8.5.0.0(1)</version>
</networkLocaleInfo>
<deviceSecurityMode>1</deviceSecurityMode>
<TLSResumptionTimer>3600</TLSResumptionTimer>
<idleTimeout>0</idleTimeout>
<authenticationURL></authenticationURL>
<directoryURL></directoryURL>
<idleURL></idleURL>
<informationURL></informationURL>
<messagesURL></messagesURL>
<proxyServerURL></proxyServerURL>
<servicesURL></servicesURL>
<secureAuthenticationURL></secureAuthenticationURL>
<secureDirectoryURL></secureDirectoryURL>
<secureIdleURL></secureIdleURL>
<secureInformationURL></secureInformationURL>
<secureMessagesURL></secureMessagesURL>
<secureServicesURL></secureServicesURL>
<dscpForSCCPPhoneConfig>96</dscpForSCCPPhoneConfig>
<dscpForSCCPPhoneServices>0</dscpForSCCPPhoneServices>
<dscpForCm2Dvce>96</dscpForCm2Dvce>
<transportLayerProtocol>1</transportLayerProtocol>
<phonePersonalization>0</phonePersonalization>
<rollover>0</rollover>
<singleButtonBarge>0</singleButtonBarge>
<joinAcrossLines>0</joinAcrossLines>
<autoCallPickupEnable>false</autoCallPickupEnable>
<blfAudibleAlertSettingOfIdleStation>0</blfAudibleAlertSettingOfIdleStation>
<blfAudibleAlertSettingOfBusyStation>0</blfAudibleAlertSettingOfBusyStation>
<capfAuthMode>0</capfAuthMode>
<capfList>
<capf>
<phonePort>3804</phonePort>
<processNodeName></processNodeName>
</capf>
</capfList>
<certHash></certHash>
<encrConfig>false</encrConfig>
<advertiseG722Codec>1</advertiseG722Codec>
<mobility>
<handoffdn></handoffdn>
<dtmfdn></dtmfdn>
<ivrdn></ivrdn>
<dtmfHoldCode>*81</dtmfHoldCode>
<dtmfExclusiveHoldCode>*82</dtmfExclusiveHoldCode>
<dtmfResumeCode>*83</dtmfResumeCode>
<dtmfTxfCode>*84</dtmfTxfCode>
<dtmfCnfCode>*85</dtmfCnfCode>
</mobility>
<userId>Capital4</userId>
<phoneServices  useHTTPS="true">
<provisioning>2</provisioning>
<phoneService  type="2" category="0">
<name>Voicemail</name>
<url>Application:Cisco/Voicemail</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Missed Calls</name>
<url>Application:Cisco/MissedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Received Calls</name>
<url>Application:Cisco/ReceivedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Placed Calls</name>
<url>Application:Cisco/PlacedCalls</url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Personal Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
<phoneService  type="0" category="0">
<name>Corporate Directory</name>
<url></url>
<vendor></vendor>
<version></version>
</phoneService>
</phoneServices>


</device>
'''
gxp_1615 = '''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Grandstream XML Provisioning Configuration -->
<gs_provision version="1">
<config version="1">
<!-- Forma de configuracao - TFTP -->
<P212>0</P212>

<!-- Sip Server -->
<P47>%ASTER%</P47>

<!-- Authenticate Password -->
<P34>%PASS%</P34>

<!-- SIP User ID -->
<P35>%RAMAL%</P35>

<!-- Authenticate ID -->
<P36>%RAMAL%</P36>

<!-- Nome do Ramal -->
<P3>%NOME%</P3>

<!--######### Account 2 ######## -->

<!-- Authenticate Password -->
<P406>%PASS2%</P406>

<!-- SIP User ID -->
<P404>%RAMAL2%</P404>

<!-- Authenticate ID -->
<P405>%RAMAL2%</P405>

<!-- Account Display -->
<P2480>1</P2480>

<!-- Preferred Vocoder 1 - G.722 -->
<P57>9</P57>

<!-- Preferred Vocoder 2 - PCMA -->
<P58>8</P58>

<!-- NTP Server -->
<P30>%NTP%</P30>

<!-- Time Zone (-3) -->
<P64>BRST+3</P64>

<!-- Formato da data - dd-mm-yyyy -->
<P102>2</P102>

<!-- Formato da hora - 0-24h -->
<P122>1</P122>

<!-- Voice Vlan -->
<P51></P51>

<!-- Configuracao via TFTP -->
<P212>0</P212>

<!-- Caminho da configuracao no TFTP -->
<P237>%TFTP%</P237>

<!-- Linguagem -->
<P1362>pt</P1362>

<!-- Mostrar o User ID na tela -->
<P2380>1</P2380>

<!-- Admin password for web interface -->
<P2>%WEB_PASS%</P2>

<!-- Dial Plan -->
<P290>{ ** | **x+ | x+ | #x+ | *#x+ }</P290>

<!-- Ringtone -->
<P104>3</P104>
</config>
</gs_provision>
'''
gxp_2170 = '''<?xml version="1.0" encoding="UTF-8" ?>
<!-- Grandstream XML Provisioning Configuration -->
<gs_provision version="1">
<config version="1">
<!-- Forma de configuracao - TFTP -->
<P212>0</P212>

<!-- Servidor de configuracao -->
<P237>%TFTP%</P237>

<!-- SIP Server -->
<!-- P47>%ASTER%</P47 -->

<!-- Password -->
<P34>%PASS%</P34>

<!-- SIP User ID -->
<P35>%RAMAL%</P35>

<!-- Authenticate ID -->
<P36>%RAMAL%</P36>

<!-- Nome do Ramal -->
<P3>%NOME%</P3>

<!-- #############Conta SIP 2############### -->

<!-- SIP Server -->
<P402>%ASTER2%</P402>

<!-- SIP User ID -->
<P404>%RAMAL2%</P404>

<!-- Authenticate ID -->
<P405>%RAMAL2%</P405>

<!-- Authenticate password -->
<P406>%PASS2%</P406>

<!-- #############Conta SIP 3############### -->
<!-- SIP Server -->
<P502>%ASTER3%</P502>

<!-- SIP User ID -->
<P504>%RAMAL3%</P504>

<!-- Authenticate ID -->
<P505>%RAMAL3%</P505>

<!-- Authenticate password -->
<P506>%PASS3%</P506>

<!-- Preferencia 1 de Codec - G.722 -->
<P57>9</P57>

<!-- Preferencia 2 de Codec - PCMA -->
<P58>8</P58>

<!-- NTP Server -->
<P30>%NTP%</P30>

<!-- Formato da data - dd-mm-yyyy -->
<P102>2</P102>

<!-- Mostrar data na barra superior -->
<P8387>1</P8387>

<!-- Formato da hora - 0-24h -->
<P122>1</P122>

<!-- Time Zone (-3) -->
<P64>BRST+3</P64>

<!-- Descanso de Tela -->
<P2918>0</P2918>

<!-- Desligar o bluetooth -->
<P2910>0</P2910>

<!-- Wallpaper download -->
<P2916>1</P2916>

<!-- Caminho do wallpaper -->
<P2917>tftp://%TFTP%/wp2170.jpg</P2917>

<!-- Voice Vlan -->
<P51></P51>

<!-- Linguagem -->
<P1362>pt</P1362>

<!-- Admin password for web interface -->
<P2>%WEB_PASS%</P2>

<!-- Dial Plan -->
<P290>{ ** | **x+ | x+ | #x+ | *#x+ }</P290>

<!-- Previsao do tempo -->
<P1402>0</P1402>

</config>
</gs_provision>
'''
yealink_22p = '''#!version:1.0.0.1
#File header "#!version:1.0.0.1" cannot be edited or deleted.##
#Line1 settings
#Activate/Deactivate the account1, 0-Disabled (Default), 1-Enabled
account.1.enable = %enable1%
#Configure the label of account1 which will display on the LCD screen
account.1.label = %name%
#Configure the display name of account1
account.1.display_name = %name%
#Configure the user name and password for register authentication
account.1.auth_name = %linha1%
account.1.password = %pass1%
#Configure the register user name
account.1.user_name = %linha1%
#Configure the SIP server address and port (5060 by default)
account.1.sip_server_host = %asterisk1%
account.1.sip_server_port = 5060
#Line2 settings
#Activate/Deactivate account2, 0-Disabled(Default), 1-Enabled
account.2.enable = %enable2%
#Configure the label of account2 which will display on the LCD screen
account.2.label =
#Configure the display name of account2
account.2.display_name =
#Configure the user name and password for register authentication
account.2.auth_name = %linha2%
account.2.password = %pass2%
#Configure the register user name
account.2.user_name = %linha2%
#Configure the SIP server address and port(5060 by default)
account.2.sip_server_host = %asterisk2%
account.2.sip_server_port = 5060
#Line3 settings
#Activate/Deactivate the account3, 0-Disabled(Default), 1-Enabled
account.3.enable = %enable3%
#Configure the label of account3 which will display on the LCD screen
account.3.label =
#Configure the display name of account3
account.3.display_name =
#Configure the user name and password for register authentication
account.3.auth_name = %linha3%
account.3.password = %pass3%
#Configure the register user name
account.3.user_name = %linha3%
#Configure the SIP server address and port (5060 by default)
account.3.sip_server_host = %asterisk3%
account.3.sip_server_port = 5060
#Configure the NTP Server
local_time.ntp_server1 = %ntp%
local_time.time_zone = -3
local_time.time_zone_name = Brazil(DST)
'''

#Entrada de Dados
os.system('clear')
input('Para prosseguir, é necessário que uma planilha esteja com extensão ".xlsx" \
e que esteja salvo na pasta "/srv/tftp/".\n\nPressione qualquer tecla para continuar...')
os.system('clear')
pass_asterisk = input("Qual a senha de registro dos telefones?\n")
check_tel = input("\nVão ser configurados telefones GrandStream? (s ou n):")


if check_tel == 's':
    pass_web = input('\nQual senha será utilizada para acesso WEB dos telefones?\n')

    create_model(path_dest_models + 'cfggxp1615.xml', gxp1625_model)
    create_model(path_dest_models + 'cfggxp1625.xml', gxp1625_model)
    create_model(path_dest_models + 'cfggxp2170.xml', gxp2170_model)

    print('\nArquivos de configuração padrão dos modelos GXP1615, GXP1625 e GXP2170 foram criados')

    input('Pressione "Enter" para prosseguir...')


while True:
    os.system('clear')

    vlan_ask = input('Qual VLAN deseja criar?\n')
    ip_ask = input(f'\nQual IP do asterisk da vlan {vlan_ask}?\n')
    vlans_dic[vlan_ask] = ip_ask
        
    while True:
        continue_ask = input("\nDeseja criar outra VLAN? [s ou n]\n")
        
        if continue_ask == 's':
            continue_ask_2 = 1
            break

        elif continue_ask == 'n':
            continue_ask_2 = 0
            break

        else:
            input('\nOpção incorreta. Pressione qualquer tecla e tente novamente...')
            os.system('clear')
        
    if continue_ask_2 == 1:
        continue

    elif continue_ask_2 == 0:
        break
os.system('clear')

print(f'Antes de prosseguir, confirme as seguintes informações:')

vlans_list = list(vlans_dic)

for item in vlans_list:
    print(f'Vlan {item} > {vlans_dic[item]}') 

input('\nPressione "Enter" para continuar...')

os.system("clear")

# Seleção da planilha e da página

stdout = shell(f'ls {path_planilha} | grep xlsx')
stdout = stdout.split('\n')

questions_wb = [
    inquirer.List('wb', message='Selecione a planilha: ', choices=stdout, default=stdout[0])
]

answers_wb = inquirer.prompt(questions_wb)


wb = openpyxl.load_workbook(path_planilha + answers_wb['wb'])
sheets = wb.sheetnames

questions_sheet = [
    inquirer.List('sheet', message='Qual a página que você deseja ler? ', choices=sheets)
]

answers_sheet = inquirer.prompt(questions_sheet)

print(answers_sheet['sheet'])


teste = path_planilha + answers_wb['wb']
print('DEBUG')
print(teste)


# Abrindo Planilha e Página
workbook = openpyxl.load_workbook(path_planilha + answers_wb['wb'])
sheet_alunos = workbook[answers_sheet['sheet']]

for indice, linha in enumerate(sheet_alunos.iter_rows(min_row=2)):

    # Etapa de tratamento do modelo apresentado na planilha
        modelo = linha[0].value
        try:
            modelo = modelo.lower().strip()
        except AttributeError as e:
            break
        # Verifica se o valor do modelo está especificado corretamente, através de uma lista
        for modelos in lista_modelos:
            modelos = re.search(modelos, modelo)
            if modelos:
                model_listed = True
                break
            else:
                model_listed = False

        if model_listed == False:
            print(f'O modelo {modelo} está incorreto')
            continue

        # Captura os demais campos da planilha, caso o modelo seja válido
        mac_ramal = linha[1].value
        mac_ramal = str(mac_ramal)
        mac_ramal = correcao_mac(mac_ramal)
        num_linha1 = linha[2].value
        num_linha2 = linha[3].value
        num_linha3 = linha[4].value
        nome_ramal = linha[5].value
        num_linha1_bool = bool(num_linha1)
        num_linha2_bool = bool(num_linha2)
        num_linha3_bool = bool(num_linha3)
        num_vlan = linha[6].value
        num_vlan_bool = bool(num_vlan)

        try:
            if num_linha1_bool == True:


                if re.search(r'gxp-?2170', modelo):
                    new_name = mac_ramal.lower()
                    new_name = path_dest_macfiles + 'cfg' + new_name + '.xml'
                    new_name = new_name.replace(' ','')

                    shell(f'touch {new_name}')
                    write_text(new_name, gxp_2170)

                    replace_pat(new_name, '%NTP%', '')
                    replace_pat(new_name, '%TFTP%', '')
                    replace_pat(new_name, '%WEB_PASS%', str(pass_web))


                    if num_linha1_bool == True:
                        replace_pat(new_name, '%RAMAL%', str(num_linha1))
                        replace_pat(new_name, '%PASS%', str(pass_asterisk))

                        if bool(nome_ramal) == True:
                            replace_pat(new_name, '%NOME%', nome_ramal)
                        else:
                            replace_pat(new_name, '%NOME%', '')

                        if num_vlan_bool == True:
                            num_vlan = str(num_vlan)
                            num_vlan = num_vlan.strip()
                            replace_pat(new_name, '%ASTER%', vlans_dic[num_vlan])

                        else:
                            print('Não existe vlan associada')

                    else:
                        replace_pat(new_name, '%RAMAL%', '')
                        replace_pat(new_name, '%NOME%', '')
                        replace_pat(new_name, '%ASTER%', '')
                        replace_pat(new_name, '%PASS%', '')


                    if num_linha2_bool == True:
                        replace_pat(new_name, '%RAMAL2%', str(num_linha2))
                        replace_pat(new_name, '%ASTER2%', str(ip_asterisk))
                        replace_pat(new_name, '%PASS2%', str(pass_asterisk))


                    else:
                        replace_pat(new_name, '%RAMAL2%', '')
                        replace_pat(new_name, '%NOME2%', '')
                        replace_pat(new_name, '%ASTER2%', '')
                        replace_pat(new_name, '%PASS2%', '')


                    if num_linha3_bool == True:
                        replace_pat(new_name, '%RAMAL3%', str(num_linha3))
                        replace_pat(new_name, '%ASTER3%', str(ip_asterisk))
                        replace_pat(new_name, '%PASS3%', str(pass_asterisk))


                    else:
                        replace_pat(new_name, '%RAMAL3%', '')
                        replace_pat(new_name, '%ASTER3%', '')
                        replace_pat(new_name, '%PASS3%', '')


                elif re.search(r'gxp-?1615', modelo):
                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.lower()
                        new_name = path_dest_macfiles + 'cfg' + new_name + '.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, gxp_1615)

                        replace_pat(new_name, '%NTP%', '')
                        replace_pat(new_name, '%TFTP%', '')
                        replace_pat(new_name, '%WEB_PASS%', str(pass_web))


                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))


                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)


                            else:
                                replace_pat(new_name, '%NOME%', '')

                            if num_vlan_bool == True:
                                num_vlan = str(num_vlan)
                                num_vlan = num_vlan.strip()
                                replace_pat(new_name, '%ASTER%', vlans_dic[num_vlan])

                            else:
                                print('Não existe vlan associada')


                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%NOME%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')


                        if num_linha2 == True:
                            replace_pat(new_name, '%RAMAL2%', str(num_linha2))
                            replace_pat(new_name, '%PASS2%', pass_asterisk)
                        else:
                            replace_pat(new_name, '%RAMAL2%', '')
                            replace_pat(new_name, '%PASS2%', '')
                    else:
                        print('* * * * Não Existe MAC associado * * * *')


                elif re.search(r'gxp-?1625', modelo):
                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.lower()
                        new_name = path_dest_macfiles + 'cfg'  + new_name + '.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, gxp_1615)

                        replace_pat(new_name, '%NTP%', '')
                        replace_pat(new_name, '%TFTP%', '')
                        replace_pat(new_name, '%WEB_PASS%', str(pass_web))

                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))

                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)


                            else:

                                replace_pat(new_name, '%NOME%', '')

                            if num_vlan_bool == True:
                                num_vlan = str(num_vlan)
                                num_vlan = num_vlan.strip()
                            
                            if num_vlan_bool == True:
                                num_vlan = str(num_vlan)
                                num_vlan = num_vlan.strip()
                                replace_pat(new_name, '%ASTER%', vlans_dic[num_vlan])

                            else:
                                print('Não existe vlan associada')

                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%NOME%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')


                        if num_linha2 == True:
                            replace_pat(new_name, '%RAMAL2%', str(num_linha2))
                            replace_pat(new_name, '%PASS2%', pass_asterisk)
                        else:
                            replace_pat(new_name, '%RAMAL2%', '')
                            replace_pat(new_name, '%PASS2%', '')
                    else:
                        print('* * * * Não Existe MAC associado * * * *')


                elif modelo == 't22p':
                    new_name = mac_ramal.lower()
                    new_name = path_dest_macfiles + new_name + '.cfg'
                    new_name = new_name.replace(' ','')

                    shell(f'touch {new_name}')
                    write_text(new_name, yealink_22p)
                    replace_pat(new_name, '%ntp%', ...)


                    if num_linha1_bool == True:
                        replace_pat(new_name,'%enable1%', '1')
                        replace_pat(new_name, '%linha1%', str(num_linha1))
                        replace_pat(new_name, '%asterisk1%', str(ip_asterisk))
                        replace_pat(new_name, '%pass1%', str(pass_asterisk))

                        if bool(nome_ramal) == True:
                            replace_pat(new_name, '%name%', nome_ramal)
                        else:
                            replace_pat(new_name, '%name%', '')


                    else:
                        replace_pat(new_name, '%enable1%', '0')
                        replace_pat(new_name, '%name%', '')
                        replace_pat(new_name, '%linha1%', '')
                        replace_pat(new_name, '%asterisk1%', '')
                        replace_pat(new_name, '%pass1%', '')


                    if num_linha2_bool == True:
                        replace_pat(new_name,'%enable2%', '1')
                        replace_pat(new_name, '%linha2%', str(num_linha2))
                        replace_pat(new_name, '%asterisk2%', str(ip_asterisk))
                        replace_pat(new_name, '%pass2%', str(pass_asterisk))


                    else:
                        replace_pat(new_name, '%enable2%', '0')
                        replace_pat(new_name, '%linha2%', '')
                        replace_pat(new_name, '%asterisk2%', '')
                        replace_pat(new_name, '%pass2%', '')


                    if num_linha3_bool == True:
                        replace_pat(new_name,'%enable3%', '1')
                        replace_pat(new_name, '%linha3%', str(num_linha3))
                        replace_pat(new_name, '%asterisk3%', str(ip_asterisk))
                        replace_pat(new_name, '%pass3%', str(pass_asterisk))


                    else:
                        replace_pat(new_name, '%enable3%', '0')
                        replace_pat(new_name, '%linha3%', '')
                        replace_pat(new_name, '%asterisk3%', '')
                        replace_pat(new_name, '%pass3%', '')

                elif re.search(r'cp-?3905', modelo):
                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.upper()
                        new_name = path_dest_macfiles + 'SEP' + new_name + '.cnf.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, cp_3905)

                        replace_pat(new_name, '%NTP%', '')

                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))

                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)

                            else:
                                replace_pat(new_name, '%NOME%', '')

                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')
                            replace_pat(new_name, '%NOME%', '')

                    else:
                        print('* * * * Não Existe MAC associado * * * *')

                elif re.search(r'cp-?7821', modelo):
                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.upper()
                        new_name = path_dest_macfiles + 'SEP' + new_name + '.cnf.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, cp_7821)

                        replace_pat(new_name, '%NTP%', '')

                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))

                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)


                            else:
                                replace_pat(new_name, '%NOME%', '')

                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')
                            replace_pat(new_name, '%NOME%', '')

                    else:
                        print('* * * * Não Existe MAC associado * * * *')



                elif re.search(r'cp-?8845', modelo):
                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.upper()
                        new_name = path_dest_macfiles + 'SEP' + new_name + '.cnf.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, cp_8845)

                        replace_pat(new_name, '%NTP%', '')

                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))

                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)


                            else:
                                replace_pat(new_name, '%NOME%', '')

                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')
                            replace_pat(new_name, '%NOME%', '')

                    else:
                        print('* * * * Não Existe MAC associado * * * *')

                elif re.search(r'cp-?8865', modelo):

                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.upper()
                        new_name = path_dest_macfiles + 'SEP' + new_name + '.cnf.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, cp_8865)

                        replace_pat(new_name, '%NTP%', '')

                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))

                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)


                            else:
                                replace_pat(new_name, '%NOME%', '')


                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')
                            replace_pat(new_name, '%NOME%', '')

                    else:
                        print('* * * * Não Existe MAC associado * * * *')


                elif re.search(r'cp-?7942', modelo):

                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.upper()
                        new_name = path_dest_macfiles + 'SEP' + new_name + '.cnf.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, cp_7942)

                        replace_pat(new_name, '%NTP%', '')

                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))

                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)


                            else:
                                replace_pat(new_name, '%NOME%', '')

                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')
                            replace_pat(new_name, '%NOME%', '')

                    else:
                        print('* * * * Não Existe MAC associado * * * *')

                elif re.search(r'cp-?9845', modelo):

                    if bool(mac_ramal) == True:
                        new_name = mac_ramal.upper()
                        new_name = path_dest_macfiles + 'SEP' + new_name + '.cnf.xml'
                        new_name = new_name.replace(' ','')

                        shell(f'touch {new_name}')
                        write_text(new_name, cp_9845)

                        replace_pat(new_name, '%NTP%', '')

                        if num_linha1_bool == True:
                            replace_pat(new_name, '%RAMAL%', str(num_linha1))
                            replace_pat(new_name, '%ASTER%', str(ip_asterisk))
                            replace_pat(new_name, '%PASS%', str(pass_asterisk))

                            if bool(nome_ramal) == True:
                                replace_pat(new_name, '%NOME%', nome_ramal)


                            else:
                                replace_pat(new_name, '%NOME%', '')


                        else:
                            replace_pat(new_name, '%RAMAL%', '')
                            replace_pat(new_name, '%ASTER%', '')
                            replace_pat(new_name, '%PASS%', '')
                            replace_pat(new_name, '%NOME%', '')

                    else:
                        print('* * * * Não Existe MAC associado * * * *')
            else:
                print(f'* * * * O MAC {mac_ramal} não possui ramal associado ou informação foi prenchida incorretamente * * * *')

        except:
            print('Fim da Planilha')
for arquivo in os.listdir(path_dest_macfiles):
    if arquivo.endswith('.xml'):
        quant_arquivos += 1
    elif arquivo.endswith('.cfg'):
        quant_arquivos += 1
print('\n* * * * Fim da Planilha! * * * *\n')
print(f'* * * * Foram gerados {quant_arquivos} arquivos de configuração * * * *\n')

