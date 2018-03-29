using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;


namespace Spotlight_Desktop
{
    internal static class Program
    {
        private static string _currSpotlightPath;

        private const bool RunOnce = false;

        const int SetWallpaper = 20;
        const int UpdateIniFile = 0x01;
        const int SendWinIniChange = 0x02;


        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);


        private static void ChangeWallpaper(string pathToImage)
        {
            SystemParametersInfo(SetWallpaper, 0, pathToImage, UpdateIniFile | SendWinIniChange);
        }


        private static void UpdateDesktop()
        {
            _currSpotlightPath = FindImage.FindCurrentImage();
            Console.WriteLine("The current Spotlight Lock Screen image is located at:\n" + _currSpotlightPath + "\n");
            ChangeWallpaper(_currSpotlightPath);
        }


        // Show output only if in a command prompt
        [DllImport("kernel32.dll")]
        private static extern void AttachConsole(int dwProcessId);


        private static void Main()
        {
            AttachConsole(-1);

            // Check if there is a new update.exe that needs to be replaced
            if (File.Exists("update_new.exe"))
            {
                if (File.Exists("update.exe"))
                {
                    try
                    {
                        File.Delete("update.exe");
                        File.Move("update_new.exe", "update.exe");
                    }
                    catch (UnauthorizedAccessException)
                    {
                        Console.WriteLine("Running while update.exe is running");
                    }
                }
            }

            int count = 0;
            while (true)
            {
                // Run every minute
                string lastestCurrentImage = FindImage.FindCurrentImage();
                if (_currSpotlightPath != lastestCurrentImage)
                {
                    _currSpotlightPath = lastestCurrentImage;
                    UpdateDesktop();
                }

                // Run twice a day
                if ((count % 60 * 12) == 0 && File.Exists("update.exe"))
                {
                    System.Diagnostics.Process.Start("update.exe");
                    count = 0;
                }

                if (RunOnce) break;

                // Check every minute
                Thread.Sleep(60 * 1000);
                count++;
            }
        }
    }
}
