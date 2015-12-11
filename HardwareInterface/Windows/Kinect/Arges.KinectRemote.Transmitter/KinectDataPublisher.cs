﻿using System;
using System.Collections.Generic;
using Arges.KinectRemote.BodyProcessor;
using Arges.KinectRemote.Data;
using Arges.KinectRemote.Transport;
using Arges.KinectRemote.Sensor;

namespace Arges.KinectRemote.Transmitter
{
    /// <summary>
    /// Connects to the available Kinect sensors, encodes the body data for publishing
    /// and sends it over the wire serialized.
    /// </summary>
    /// <remarks>
    /// Currently part of the Transmitter library. I've considered moving it to
    /// the Transport library, but that would require adding a dependency on that
    /// library to Sensor, and I'd rather that remains solely where it's 
    /// necessary (since the receivers do not need to have any dependency to the
    /// sensor but do need to depend on Transport).
    /// </remarks>
    public class KinectDataPublisher
    {
        readonly MessagePublisherBase _messagePublisher;
        readonly KinectSensorManager _kinectRuntime = new KinectSensorManager();

        /// <summary>
        /// Last number of bodies sent
        /// </summary>
        private int _lastBodyCount;

        private int KinectID = 3;

        /// <summary>
        /// Is the publisher currently allowed to broadcast?
        /// </summary>
        public bool BroadcastEnabled { set; get; }

        /// <summary>
        /// List of body processors that we should run each body through 
        /// before sending it down the wire
        /// </summary>
        public List<ABodyProcessor> BodyProcessors { get; private set; }

        /// <summary>
        /// Initializes a Kinect Data Publisher
        /// </summary>
        /// <param name="ipAddress">IP Address for the RabbitMQ server</param>
        /// <param name="exchangeName">Exchange to publish information to</param>
        /// <param name="senderId">Sender ID, used as the first part of the topic</param>
        /// <param name="username">Username</param>
        /// <param name="password">Password</param>
        public KinectDataPublisher(string ipAddress, string exchangeName, string senderId, string username = "guest", string password = "guest")
        {
            _messagePublisher = new RabbitMqMessagePublisher(ipAddress, exchangeName, senderId, username, password);

            Console.WriteLine("Starting sensor");
            var frameHandler = new KinectBodyFrameHandler(_kinectRuntime);
            frameHandler.FrameReady += OnBodyFrameReady;
            _kinectRuntime.AddFrameHandler(frameHandler);
            _kinectRuntime.OpenSensor();
            Console.WriteLine("Sensor started");

            BroadcastEnabled = true;
            BodyProcessors = new List<ABodyProcessor>();
        }

        ~KinectDataPublisher()
        {
            _kinectRuntime.CloseSensor();
        }

        void OnBodyFrameReady(object sender, KinectItemListEventArgs<KinectBody> e)
        {
            if (BroadcastEnabled && e != null && e.Items != null &&
                (e.Items.Count > 0 || _lastBodyCount != 0))
            {
                ProcessAndTransmit(e.SensorId, e.Items);
                _lastBodyCount = e.Items.Count;
            }
        }

        /// <summary>
        /// Called when data is ready, creates a bundle, serializes it and broadcasts it
        /// </summary>
        /// <param name="bodies">List of bodies to send</param>
        /// <param name="sensorId">Device ID for the Kinect sensor</param>
        void ProcessAndTransmit(string sensorId, List<KinectBody> bodies)
        {
            List<string> infos;
            foreach (var processor in BodyProcessors)
            {
                processor.ProcessBodies(bodies);
            }
            for (int i = 0; i < bodies.Count; i++)
            {
                infos = getGestures(bodies[i]);
                foreach (string info in infos)
                {
                    _messagePublisher.SerializeAndSendObject(KinectID + "" + i + ":" + info, "body");
                }
                infos.Clear();
            }

        }

        List<string> getGestures(KinectBody body)
        {
            List<string> gestures = new List<string>();
            foreach (var tag in body.Tags)
            {
                string info;
                switch (tag)
                {
                    case "Sitting":
                        info = body.bodyPosition.getHeadPosition().Magnitude + ":Sitting";
                        gestures.Add(info);
                        break;
                    case "HandsUp":
                        info = body.bodyPosition.getHeadPosition().Magnitude + ":HandsUp";
                        gestures.Add(info);
                        break;
                    default:
                        break;

                }
            }
            if (body.HandLeftState == KinectHandState.Closed)
            {
                gestures.Add(body.bodyPosition.getLeftHandPosition().ToString() + ":LeftHandClosed");
            }
            if (body.HandRightState == KinectHandState.Closed)
            {
                gestures.Add(body.bodyPosition.getRightHandPosition().ToString() + ":RightHandClosed");
            }
            if (gestures.Count == 0)
            {
                gestures.Add(body.bodyPosition.getHeadPosition().ToString() + ":None");
            }
            return gestures;
        }
    }
}
