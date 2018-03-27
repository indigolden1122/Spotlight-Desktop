using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Runtime.InteropServices;


namespace Spotlight_Desktop
{
    class Program
    {
        [DllImport("kernel32.dll")]
        private static extern void AttachConsole(int dwProcessId);

        static void Main(string[] args)
        {
            AttachConsole(-1);
            Console.WriteLine("Hello World");
        }
    }
}
