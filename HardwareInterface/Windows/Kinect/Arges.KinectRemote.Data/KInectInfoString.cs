using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Arges.KinectRemote.Data
{
    class KinectInfoString 
    {

        private string message;
        private int kinectID = 3;
        private KinectBody body;
        private int bodyID;
        private string gesture;

        public KinectInfoString(KinectBody body, int num)
        {
            this.body = body;
            this.bodyID = num;
            gesture = identifyGesture();
        }

        private string identifyGesture()
        {
            HashSet<string> tags = body.Tags;
            if (tags.Contains("sitting"))
            {
                return "sitting";
            }
            return "";
        }
        public string getMessage()
        {
            message = kinectID + bodyID + ":" + body.bodyPosition.getHeadPosition().Magnitude + ":" + gesture;
            return message;
        }
    }
}
