﻿#define NoWait
using System;
using System.Configuration;
using Arges.KinectRemote.Data;
using Arges.KinectRemote.Transport;


namespace Arges.KinectRemote.TestConsole
{
    /// <summary>
    /// Connects to a RabbitMq server and logs any body messages it receives.
    /// It will not request gesture messages - see TestGestureConsole for
    /// an example.
    /// </summary>
    static class Program
    {
        private static string _exchange;
        private static string _ipAddress;
        private static string _bodyBindingKey;

        private static void ReadConfigSettings()
        {
            _exchange = ConfigurationManager.AppSettings["exchange"].Trim();
            _ipAddress = ConfigurationManager.AppSettings["ipAddress"].Trim();
            _bodyBindingKey = ConfigurationManager.AppSettings["bodyBindingKey"].Trim();

            if (string.IsNullOrEmpty(_exchange))
            {
                throw new ArgumentException("Exchange is not specified in the app.config.");
            }
            if (string.IsNullOrEmpty(_ipAddress))
            {
                Console.WriteLine("IP Address not specified. Connecting to local host.");
                _ipAddress = "127.0.0.1";
            }
            if (string.IsNullOrEmpty(_bodyBindingKey))
            {
                Console.WriteLine("Body binding key not specified. Binding to all remotes for body information.");
                _bodyBindingKey = "*.body";
            }

            Console.WriteLine("Exchange is: {0}", _exchange);
            Console.WriteLine("IP address is: {0}", _ipAddress);
            Console.WriteLine("Listening for bodies to: {0}", _bodyBindingKey);
        }

        private static void Main()
        {
            ReadConfigSettings();

            try
            {
                using (var receiver = new StringReceiver(_ipAddress, _exchange, _bodyBindingKey))
                {
                    while (true)
                    {
#if NoWait
                        // Non-blocking, will return null if there isn't any data available
                        
                        var kinectData = receiver.DequeueNoWait();
                        if (kinectData != null)
                        {
                            Console.WriteLine(kinectData);
                            //LogKinectData(kinectData);
                        }
                        System.Threading.Thread.Sleep(1);
#else
                        // Blocking call
                        var kinectData = receiver.Dequeue();
                        LogKinectData(kinectData);
#endif
                    }
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine(ex.Message);
                Console.ResetColor();
                Console.WriteLine(ex.StackTrace);
                Console.ReadLine();
            }
        }

        static void LogKinectData(KinectBag<string> bundle)
        {
            if (bundle.Items != null)
            {
                foreach (string info in bundle.Items)
                {
                    Console.WriteLine(info);
                }
            }
        }
    }
}

