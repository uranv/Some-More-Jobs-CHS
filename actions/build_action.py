import pandas as pd

if __name__ == "__main__":
    dfchs = pd.read_csv('scr_action_chs.csv')
    with open("scr_action_chs.xml","w") as f:
        f.write("<actions>\n")
    for i in range(dfchs.shape[0]):
        with open("scr_action_chs.xml","a") as f:
            if dfchs.iat[i,3]=='0':
                f.write("  <li Class='XmlExtensions.Action.SetSetting'>\n")        
            else:
                f.write("  <li Class='XmlExtensions.Action.SetSetting' MayRequire='"+dfchs.iat[i,3]+"'>\n")
            f.write("    <key>"+dfchs.iat[i,0]+"."+dfchs.iat[i,1]+"</key>\n    <value>"+dfchs.iat[i,2]+"</value>\n  </li>\n")
    with open("scr_action_chs.xml","a") as f:
        f.write("</actions>")