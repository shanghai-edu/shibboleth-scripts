import json


def get_cfg():
    f = open("cfg.json", encoding='utf-8')
    setting = json.load(f).get("ldap")
    return setting


try:
    ldap_setting = get_cfg()
    print(ldap_setting)
    idp_template = """# LDAP authentication configuration, see authn/ldap-authn-config.xml
    # Note, this doesn't apply to the use of JAAS
    
    ## Authenticator strategy, either anonSearchAuthenticator, bindSearchAuthenticator, directAuthenticator, adAuthenticator
    idp.authn.LDAP.authenticator                   = bindSearchAuthenticator
    
    ## Connection properties ##
    idp.authn.LDAP.ldapURL                          = ldap://""" + ldap_setting.get("addr") + """
    idp.authn.LDAP.useStartTLS                     = false
    #idp.authn.LDAP.useSSL                          = false
    # Time in milliseconds that connects will block
    #idp.authn.LDAP.connectTimeout                  = PT3S
    # Time in milliseconds to wait for responses
    #idp.authn.LDAP.responseTimeout                 = PT3S
    
    ## SSL configuration, either jvmTrust, certificateTrust, or keyStoreTrust
    #idp.authn.LDAP.sslConfig                       = certificateTrust
    ## If using certificateTrust above, set to the trusted certificate's path
    idp.authn.LDAP.trustCertificates                = %{idp.home}/credentials/ldap-server.crt
    ## If using keyStoreTrust above, set to the truststore path
    idp.authn.LDAP.trustStore                       = %{idp.home}/credentials/ldap-server.truststore
    
    ## Return attributes during authentication
    idp.authn.LDAP.returnAttributes                 = passwordExpirationTime,loginGraceRemaining
    
    ## DN resolution properties ##
    
    # Search DN resolution, used by anonSearchAuthenticator, bindSearchAuthenticator
    # for AD: CN=Users,DC=example,DC=org
    idp.authn.LDAP.baseDN                           = """ + ldap_setting.get('baseDn') + """
    idp.authn.LDAP.subtreeSearch                    = true
    idp.authn.LDAP.userFilter                       = """ + ldap_setting.get('authFilter').replace('(&', '').replace(')', '', 1).replace('%s', '{user}') + """
    # bind search configuration
    # for AD: idp.authn.LDAP.bindDN=adminuser@domain.com
    idp.authn.LDAP.bindDN                           = """ + ldap_setting.get("bindDn") + """
    idp.authn.LDAP.bindDNCredential                 = """ + ldap_setting.get("bindPass") + """
    
    # Format DN resolution, used by directAuthenticator, adAuthenticator
    # for AD use idp.authn.LDAP.dnFormat=%s@domain.com
    idp.authn.LDAP.dnFormat                         = uid=%s, """ + ldap_setting.get('baseDn') + """
    
    # LDAP attribute configuration, see attribute-resolver.xml
    # Note, this likely won't apply to the use of legacy V2 resolver configurations
    idp.attribute.resolver.LDAP.ldapURL             = %{idp.authn.LDAP.ldapURL}
    idp.attribute.resolver.LDAP.connectTimeout      = %{idp.authn.LDAP.connectTimeout:PT3S}
    idp.attribute.resolver.LDAP.responseTimeout     = %{idp.authn.LDAP.responseTimeout:PT3S}
    idp.attribute.resolver.LDAP.baseDN              = %{idp.authn.LDAP.baseDN:undefined}
    idp.attribute.resolver.LDAP.bindDN              = %{idp.authn.LDAP.bindDN:undefined}
    idp.attribute.resolver.LDAP.bindDNCredential    = %{idp.authn.LDAP.bindDNCredential:undefined}
    idp.attribute.resolver.LDAP.useStartTLS         = %{idp.authn.LDAP.useStartTLS:true}
    idp.attribute.resolver.LDAP.trustCertificates   = %{idp.authn.LDAP.trustCertificates:undefined}
    idp.attribute.resolver.LDAP.searchFilter        = (uid=$resolutionContext.principal)
    
    # LDAP pool configuration, used for both authn and DN resolution
    #idp.pool.LDAP.minSize                          = 3
    #idp.pool.LDAP.maxSize                          = 10
    #idp.pool.LDAP.validateOnCheckout               = false
    #idp.pool.LDAP.validatePeriodically             = true
    #idp.pool.LDAP.validatePeriod                   = PT5M
    #idp.pool.LDAP.prunePeriod                      = PT5M
    #idp.pool.LDAP.idleTime                         = PT10M
    #idp.pool.LDAP.blockWaitTime                    = PT3S
    #idp.pool.LDAP.failFastInitialize               = false"""

    ldp_xml = open('ldap.properties', 'w')
    ldp_xml.write(idp_template)
except Exception as e:
    print(e)
