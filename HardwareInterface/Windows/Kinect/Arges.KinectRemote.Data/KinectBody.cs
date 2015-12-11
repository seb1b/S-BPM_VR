﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using ProtoBuf;

namespace Arges.KinectRemote.Data
{
    /// <summary>
    /// Encapsulates data for a single body
    /// </summary>
    [Serializable, ProtoContract]
    public class KinectBody
    {
        #region Properties

        /// <summary>
        /// Current Body Id
        /// </summary>
        [ProtoMember(1)] public readonly string BodyId;

        /// <summary>
        /// Collection of Joints
        /// </summary>
        [ProtoMember(2)] public KinectJoint[] Joints;

        /// <summary>
        /// Left hand state from the list of possible Kinect hand states
        /// </summary>
        [ProtoMember(4)] public KinectHandState HandLeftState;

        /// <summary>
        /// Right hand state from the list of possible Kinect hand states
        /// </summary>
        [ProtoMember(5)] public KinectHandState HandRightState;

        /// <summary>
        /// Confidence for the left hand state
        /// </summary>
        [ProtoMember(6)] public float HandLeftConfidence;

        /// <summary>
        /// Confidence for the right hand state
        /// </summary>
        [ProtoMember(7)] public float HandRightConfidence;

        /// <summary>
        /// Application-specific body priority
        /// </summary>
        /// <remarks>
        /// Meant for processing in the remote, for example to indicate if
        /// here is a particular user who we want to designate as the main
        /// one. The meaning will be application-specific.
        /// </remarks>
        [ProtoMember(8)] public int Priority;

        /// <summary>
        /// Lean amounts for the body. Left/Right corresponds to the X,
        /// Forward/Back to the Y.
        /// </summary>
        [ProtoMember(9)] public KinectPoint Lean;

        /// <summary>
        /// Lean tracking state.
        /// </summary>
        [ProtoMember(10)] public KinectTrackingState LeanTrackingState;

        /// <summary>
        /// Original Tracking ID for the body from the sensor
        /// </summary>
        [ProtoMember(11)] public readonly ulong TrackingId;

        /// <summary>
        /// Custom float values calculated by a body processor to be sent over the wire
        /// </summary>
        /// <remarks>
        /// We may want to have a body processor calculate some body- or joint-
        /// related information, to relieve the load from the client site. Use
        /// this property to send these values.
        /// </remarks>
        [ProtoMember(12)] public Dictionary<string, float> FloatData = new Dictionary<string, float>();

        /// <summary>
        /// Custom Vector3 values calculated by a body processor to be sent over the wire
        /// </summary>
        /// <remarks>
        /// We may want to have a body processor calculate some body- or joint-
        /// related information, to relieve the load from the client site. Use
        /// this property to send these values if they're vectors.
        /// </remarks>
        [ProtoMember(13)] public Dictionary<string, KinectVector3> Vector3Data = new Dictionary<string, KinectVector3>();

        /// <summary>
        /// List of tags related to this body
        /// </summary>
        /// <remarks>Will hold an arbitrary set of body tags, for instance "Cached" or "Sitting" </remarks>
        [ProtoMember(14)] public HashSet<string> Tags = new HashSet<string>();

        [ProtoMember(15)]
        public KinectBodyPosition bodyPosition;




        /// <summary>
        /// Indexes the joints by KinectJointType
        /// </summary>
        /// <param name="jointType">Joint type</param>
        /// <returns>Corresponding KinectJoint</returns>
        public KinectJoint this[KinectJointType jointType]
        {
            get { return Joints[(int) jointType]; }
            set { Joints[(int) jointType] = value; }
        }

        #endregion

        public KinectBody()
        {
            bodyPosition = new KinectBodyPosition(this);
        }

        public KinectBody(string sensorId, ulong trackingId)
        {
            // Add an identifier using the sensor ID to keep the body entity unique across all devices.
            BodyId = string.Format("{0}.{1}", sensorId, trackingId);
            TrackingId = trackingId;
            bodyPosition = new KinectBodyPosition(this);
        }

        /// <summary>
        /// Offsets joints to a particular distance.
        /// </summary>
        /// <param name="x">X offset</param>
        /// <param name="y">Y offset</param>
        /// <param name="z">Z offset</param>
        public void ApplyOffset(float x, float y, float z)
        {
            if (Joints == null)
            {
                return;
            }
            foreach (var joint in Joints)
            {
                joint.Position.X += x;
                joint.Position.Y += y;
                joint.Position.Z += z;
            }
        }

        public override string ToString()
        {
            return string.Format("Id: {0} Tags: {1}", BodyId, string.Join(", ", Tags.ToArray()));
        }

        /// <summary>
        /// Evaluates if a joint in the body is inferred
        /// </summary>
        /// <param name="jointType">Joint type to look for</param>
        /// <returns>Returns true if the joint is inferred or null, false if it is not or it isn't found</returns>
        public bool IsJointInferred(KinectJointType jointType)
        {
            return this[jointType] == null || this[jointType].TrackingState == KinectTrackingState.Inferred;
        }

        /// <summary>
        /// Resets the data values on the custom body data
        /// </summary>
        /// <remarks>
        /// Notice that we don't just clear the list, since a receiver may be
        /// expecting to receive them, but instead reset them to the baseline,
        /// since some receivers may expect to always get at least the default.
        /// </remarks>
        public void ResetData()
        {
            foreach (var k in Vector3Data.Keys.ToList())
            {
                Vector3Data[k] = KinectVector3.Zero;
            }
            foreach (var k in FloatData.Keys.ToList())
            {
                FloatData[k] = 0;
            }
            Tags.Clear();
        }
    }


    [ProtoContract]
    public enum KinectHandState
    {
        Unknown = 0,
        NotTracked = 1,
        Open = 2,
        Closed = 3,
        Lasso = 4,
    }


    [ProtoContract]
    public enum KinectJointType
    {
        SpineBase = 0,
        SpineMid = 1,
        Neck = 2,
        Head = 3,
        ShoulderLeft = 4,
        ElbowLeft = 5,
        WristLeft = 6,
        HandLeft = 7,
        ShoulderRight = 8,
        ElbowRight = 9,
        WristRight = 10,
        HandRight = 11,
        HipLeft = 12,
        KneeLeft = 13,
        AnkleLeft = 14,
        FootLeft = 15,
        HipRight = 16,
        KneeRight = 17,
        AnkleRight = 18,
        FootRight = 19,
        SpineShoulder = 20,
        HandTipLeft = 21,
        ThumbLeft = 22,
        HandTipRight = 23,
        ThumbRight = 24
    }
}