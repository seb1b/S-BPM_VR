using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Arges.KinectRemote.Data
{
    public class KinectBodyPosition
    {
        private KinectBody body;
        public KinectBodyPosition(KinectBody body)
        {
            this.body = body;
        }
        public KinectVector3 getHeadPosition()
        {
            
            var head = body.Joints.FirstOrDefault(j => j.JointType == KinectJointType.Head);
            KinectVector3 pos = new KinectVector3(head.Position.X, head.Position.Y, head.Position.Z);
            return pos;
        }

        public KinectVector3 getLeftHandPosition()
        {

            var leftHand = body.Joints.FirstOrDefault(j => j.JointType == KinectJointType.HandLeft);
            KinectVector3 pos = new KinectVector3(leftHand.Position.X, leftHand.Position.Y, leftHand.Position.Z);
            return pos;
        }

        public KinectVector3 getRightHandPosition()
        {

            var rightHand = body.Joints.FirstOrDefault(j => j.JointType == KinectJointType.HandRight);
            KinectVector3 pos = new KinectVector3(rightHand.Position.X, rightHand.Position.Y, rightHand.Position.Z);
            return pos;
        }
    }

   
}
