using System;
using System.Runtime.InteropServices;


namespace Spotlight_Desktop
{
    internal class Program
    {
        private static string _currSpotlightPath;

        private static void ChangeWallpaper(string pathToImage)
        {
            // This should do that^
        }

        // Show output only if in a command prompt
        [DllImport("kernel32.dll")]
        private static extern void AttachConsole(int dwProcessId);

        private static void Main(string[] args)
        {
            AttachConsole(-1);
            _currSpotlightPath = FindImage.FindCurrentImage();

            Console.WriteLine("The current Spotlight Lock Screen image is located at:\n" + _currSpotlightPath);

            ChangeWallpaper(_currSpotlightPath);
        }
    }
}
