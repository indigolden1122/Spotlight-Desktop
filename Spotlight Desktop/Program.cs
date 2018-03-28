using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Threading;


namespace Spotlight_Desktop
{
    internal class Program
    {
        private static string _currSpotlightPath;


        private static void ChangeWallpaper(string pathToImage)
        {
            // This should do that^
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

        private static void Main(string[] args)
        {
            AttachConsole(-1);
            _currSpotlightPath = FindImage.FindCurrentImage();

            while (true)
            {
                // Run every minute
                if (_currSpotlightPath != FindImage.FindCurrentImage()) UpdateDesktop();

                // Check every minute
                Thread.Sleep(60 * 1000);
            }
        }
    }
}
