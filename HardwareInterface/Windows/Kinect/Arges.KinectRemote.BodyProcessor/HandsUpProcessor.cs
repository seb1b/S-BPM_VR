using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Arges.KinectRemote.Data;

namespace Arges.KinectRemote.BodyProcessor
{
    public class HandsUpProcessor : ABodyProcessor
    {
        public HandsUpProcessor()
        {

        }

        protected override bool ProcessBody(KinectBody body)
        {
            var Shoulder = body.Joints.FirstOrDefault(j => j.JointType == KinectJointType.SpineShoulder);
            var leftHand = body.Joints.FirstOrDefault(j => j.JointType == KinectJointType.HandLeft);
            var rightHand = body.Joints.FirstOrDefault(j => j.JointType == KinectJointType.HandRight);
            if (Shoulder.Position.Y >= leftHand.Position.Y && Shoulder.Position.Y >= rightHand.Position.Y) {
                body.Tags.Add("HandsUp");
                return true;
            } else
            {
                return false;
            }
        }
    }
}
