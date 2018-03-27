using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Spotlight_Desktop
{
    static class FindImage
    {
        private const string CreativePath = @"SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Creative";

        private const string OldCreativePath =
            @"SOFTWARE\Microsoft\Windows\CurrentVersion\Lock Screen\Creative";
        private static readonly string UserLocalAppData =
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);


        // This is done in a specifc order
        // ...\LogonUI\Creative\[Phase 1]\[Phase 2]
        public static string FindCurrentImage()
        {
            // Check the Creative subkeys
            var creative = new RegLookupParse(CreativePath);

            // *Currently used on the latest Windows 10 Release*
            // This goes through [Phase 1] SubKeys, then the last [Phase 2] SubKey
            foreach (RegLookupParse.SubKey currentPhase1Key in creative.SubKeys)
            {
                if (currentPhase1Key.SubKeyObj.SubKeys.Count != 0)
                {
                    // Okay, there is a [Phase 2] Sub Key, find the last one and go through it's Values in search of "landscapeImage"
                    foreach (RegLookupParse.KeyValue phase2KeyValue in currentPhase1Key.SubKeyObj.SubKeys.Last().SubKeyObj.KeyValues)
                    {
                        if (phase2KeyValue.Name == "landscapeImage")
                        {
                            // Check to make sure it belongs to this account
                            if (phase2KeyValue.Value.StartsWith(UserLocalAppData)) return phase2KeyValue.Value;
                            break;
                        }
                    }
                }
            }

            // This goes through [Phase 1] SubKeys, and searches it's Key Values for "LandscapeAssetPath"
            // (Used for an older Windows 10 update where [Phase 2] didn't exsist)
            // (This does not go into [Phase 2])
            foreach (RegLookupParse.SubKey currentPhase1Key in creative.SubKeys)
            {
                // We have a [Phase 2] SubKey, now find the "landscapeImage" in the KeyValues
                foreach (RegLookupParse.KeyValue phase2KeyValue in currentPhase1Key.SubKeyObj.KeyValues)
                {
                    if (phase2KeyValue.Name == "LandscapeAssetPath")
                    {
                        // Check to make sure it belongs to this account
                        if (phase2KeyValue.Value.StartsWith(UserLocalAppData)) return phase2KeyValue.Value;
                        break;
                    }
                }
            }

            // Should occur if on an old Windows Update
            var oldCreative = new RegLookupParse(OldCreativePath, false);

            if (!oldCreative.Error)
            {
                foreach (RegLookupParse.KeyValue keyName in oldCreative.KeyValues)
                {
                    if (keyName.Name == "LandscapeAssetPath")
                    {
                        if (keyName.Value.StartsWith(UserLocalAppData)) return keyName.Value;
                    }
                }
            }

            return null;
        }
    }
}
