'''Module providing manifest tests for the SMART API Verifier'''
# Developed by: Nikolai Schwertner
#
# Revision history:
#     2012-05-14 Initial release

# Standard module imports
import string
import re

def isurl (str):
    if isinstance(str, basestring) and (str.startswith("http://") or str.startswith("https://")):
        return True
    else:
        return False

def app_manifest_structure_validator (manifest):
    '''A structure test for an app manifest's JSON'''
    
    messages = []
    
    if type(manifest) != dict:
    
        messages.append ("The manifest definition should be a dictionary")
        
    else:
    
        keys = manifest.keys()
        
        if "name" not in keys or not isinstance(manifest["name"], basestring) :
            messages.append ("All app manifests must have a 'name' string property")
            
        if "description" not in keys or not isinstance(manifest["description"], basestring) :
            messages.append ("All app manifests must have a 'description' string property")
            
        if "id" not in keys or not isinstance(manifest["id"], basestring) :
            messages.append ("All app manifests must have a 'id' string property")
            
        if "mode" not in keys or manifest["mode"] not in ("ui","background","frame_ui") :
            messages.append ("'mode' property must be one of ('ui','background','frame_ui')")
        elif manifest["mode"] in ("ui","frame_ui"):
            if "icon" not in keys or not isurl(manifest["icon"]):
                messages.append ("'icon' propery for non-background apps should be an http/https URL")
            if "index" not in keys or not isurl(manifest["index"]):
                messages.append ("'index' propery for non-background apps should be an http/https URL")
        elif manifest["mode"] == "background":
            if "icon" in keys or "index" in keys or "optimalBrowserEnvironments" in keys or "supportedBrowserEnvironments" in keys:
                messages.append ("Background apps should not have 'icon', 'index', 'supportedBrowserEnvironments', or 'optimalBrowserEnvironments' properties in their manifest")

        if "scope" in keys and not isinstance(manifest["scope"], basestring) :
            messages.append ("'scope' parameter should be a string property")
            
        if "version" in keys and not isinstance(manifest["version"], basestring) :
            messages.append ("'version' parameter should be a string property")
            
        if "author" in keys and not isinstance(manifest["author"], basestring) :
            messages.append ("'author' should be a string property")
            
        if "smart_version" in keys and not re.match("^[\d]+(?:\.[\d]+){0,2}$", manifest["smart_version"]) :
            messages.append ("'smart_version' should be of type 'major[.minor][.build]'")
            
        if "requires" in keys:
            r = manifest["requires"]
            if type(r) != dict:
                messages.append ("The 'requires' property definition should be a dictionary")
            else:
                for api in r.keys():
                    if not isurl(api):
                        messages.append ("The '%s' property should be a valid http/https url" % api)
                    if type(r[api]) != dict:
                        messages.append ("The '%s' property definition should be a dictionary" % api)
                    else:
                        if "methods" not in r[api].keys() or type(r[api]["methods"]) != list :
                            messages.append ("'%s' property should define a 'methods' list" % api)
                        else:
                            for m in r[api]["methods"]:
                                if m not in ("GET", "PUT", "POST", "DELETE"):
                                    messages.append ("'methods' list items must be one of ('GET', 'PUT', 'POST', 'DELETE')")
                        if "codes" in r[api].keys() :
                            if type(r[api]["codes"]) != list :
                                messages.append ("'codes' property should be a list")
                            else:
                                for c in r[api]["codes"]:
                                    if not isurl(c):
                                        messages.append ("'%s' should be an http/https URL" % c)
                        for k in (key for key in r[api].keys() if key not in ("methods", "codes")):
                            messages.append ("'%s' property is not part of the SMART standard" % k)
            
        for k in (key for key in keys if key not in ("name", "description", "author", "id", "version", "mode", "scope", "icon", "index", "smart_version", "requires", "optimalBrowserEnvironments", "supportedBrowserEnvironments")):
            messages.append ("'%s' property is not part of the SMART standard" % k)
        
    return messages
    
def container_manifest_structure_validator (manifest):
    '''A structure test for a container manifest's JSON'''
    
    messages = []
    
    if type(manifest) != dict:
    
        messages.append ("The manifest definition should be a dictionary")
        
    else:
    
        keys = manifest.keys()
        
        if "admin" not in keys or not isinstance(manifest["admin"], basestring) :
            messages.append ("All container manifests must have an 'admin' string property")
            
        if "api_base" not in keys or not isurl(manifest["api_base"]):
                messages.append ("The 'api_base' propery should be an http/https URL")  
              
        if "description" not in keys or not isinstance(manifest["description"], basestring) :
            messages.append ("All container manifests must have an 'description' string property")
            
        if "name" not in keys or not isinstance(manifest["name"], basestring) :
            messages.append ("All container manifests must have an 'name' string property")
            
        if "smart_version" not in keys or not isinstance(manifest["smart_version"], basestring) :
            messages.append ("All container manifests must have an 'smart_version' string property")
  
        if "launch_urls" not in keys or type(manifest["launch_urls"]) != dict:
            messages.append ("The 'launch_urls' propery should be a dictionary")
        else:
            rkeys = manifest["launch_urls"].keys()
            
            if "authorize_token" not in rkeys or not isurl(manifest["launch_urls"]["authorize_token"]):
                messages.append ("The 'authorize_token' propery should be an http/https URL")
                
            if "exchange_token" not in rkeys or not isurl(manifest["launch_urls"]["exchange_token"]):
                messages.append ("The 'exchange_token' propery should be an http/https URL")  
                
            if "request_token" not in rkeys or not isurl(manifest["launch_urls"]["request_token"]):
                messages.append ("The 'request_token' propery should be an http/https URL")  

        if "capabilities" not in keys or type(manifest["capabilities"]) != dict:
            messages.append ("The 'capabilities' property definition should be a dictionary")
        else:
            r = manifest["capabilities"]
            for api in r.keys():
                if not isurl(api):
                    messages.append ("The '%s' property should be a valid http/https url" % api)
                if type(r[api]) != dict:
                    messages.append ("The '%s' property definition should be a dictionary" % api)
                else:
                    if "methods" not in r[api].keys() or type(r[api]["methods"]) != list :
                        messages.append ("'%s' property should define a 'methods' list" % api)
                    else:
                        for m in r[api]["methods"]:
                            if m not in ("GET", "PUT", "POST", "DELETE"):
                                messages.append ("'methods' list items must be one of ('GET', 'PUT', 'POST', 'DELETE')")
                    if "codes" in r[api].keys() :
                        if type(r[api]["codes"]) != list :
                            messages.append ("'codes' property should be a list")
                        else:
                            for c in r[api]["codes"]:
                                if not isurl(c):
                                    messages.append ("'%s' should be an http/https URL" % c)
                    for k in (key for key in r[api].keys() if key not in ("methods", "codes")):
                        messages.append ("'%s' property is not part of the SMART standard" % k)
            
        for k in (key for key in keys if key not in ("admin", "api_base", "description", "name", "smart_version", "launch_urls", "capabilities")):
            messages.append ("'%s' property is not part of the SMART standard" % k)
        
    return messages
