using System;
using System.Runtime.InteropServices;


namespace Spotlight_Desktop
{
    internal class Program
    {


        // Show output only if in a command prompt
        [DllImport("kernel32.dll")]
        private static extern void AttachConsole(int dwProcessId);

        private static void Main(string[] args)
        {
            AttachConsole(-1);

            Console.WriteLine("The current Spotlight Lock Screen image is located at:\n"+ FindImage.FindCurrentImage());
        }
    }
}
