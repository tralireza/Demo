"""
Cisco RPC Payloads for IOS XR 7.3.2
-- Unified Models
-- Cisco-IOS-XR-um-interface-cfg.yang
"""

IF_CREATE, IF_DEL, COMMIT = 0, 1, 2

Payload = ['''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="%i">
  <target>
    <candidate/>
  </target>
  <config>
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-interface-cfg">
      <interface>
        <interface-name>%s</interface-name>
        <description>*** NetConf ***</description>
      </interface>
    </interfaces>
  </config>
</edit-config>''',
           '''<edit-config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="%i">
  <target>
    <candidate/>
  </target>
  <config>
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-interface-cfg">
      <interface xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
        <interface-name>%s</interface-name>
      </interface>
    </interfaces>
  </config>
</edit-config>''',
           '''<commit xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="%i" />'''
           ]
