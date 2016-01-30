using System;
using Microsoft.Kinect.VisualGestureBuilder;
using Microsoft.Kinect;
using System.Threading.Tasks;
using System.Threading;

namespace Kinect {
	public class Person {
		int kinectID = 3;
		HandState leftHandState;
		HandState rightHandState;
		HandState currentLeft;
		HandState currentRight;
		string[] message;
		Joint leftHand;
		Joint rightHand;
		int id;
		Send instance;
		Body body;

		public Person (int id) {
			this.id = id;	
			this.instance = Send.getInstance ();
			if (instance == null) {
				Console.WriteLine ("Die Instanz ist null");
			}
			leftHandState = HandState.NotTracked;
			rightHandState = HandState.NotTracked;
			message = new string[2];
		}

		public void act (Body bodyIn) {
			body = bodyIn;
			ThreadStart act = new ThreadStart (CallToActThread);
			Thread ActThread = new Thread (act);
			ActThread.Start ();
		}

		public void CallToActThread () {
			workWith ();
		}

		private void workWith () {
			leftHand = body.Joints [JointType.HandLeft];
			rightHand = body.Joints [JointType.HandRight];
			currentRight = body.HandRightState;
			currentLeft = body.HandLeftState;

			if (currentLeft != HandState.NotTracked) {
					if (currentLeft == HandState.Closed) {
					message [0] = ":" + getPosition (leftHand)+ ":L:closed";
						leftHandState = HandState.Closed;
					} else if (currentLeft == HandState.Open) {
						message [0] = ":" + getPosition (leftHand) + ":L:open";
						leftHandState = HandState.Open;
					} else {
						leftHandState = body.HandLeftState;
						message [0] = ":" + getPosition (leftHand) + ":L:unknown";
					}
					if (message [0] != "") {
						instance.sendData (kinectID + "" + id + message [0]);
					}
			}

			if (currentRight != HandState.NotTracked) {
					if (currentRight == HandState.Closed) {
						message [1] = ":" + getPosition (rightHand) + ":R:closed";
						rightHandState = HandState.Closed;
					} else if (currentRight == HandState.Open) {
						message [1] = ":" + getPosition (rightHand) + ":R:open";
						rightHandState = HandState.Open;
					} else {
						rightHandState = body.HandRightState;
						message [1] = ":" + getPosition (rightHand) + ":R:unknown";
					} 
					if (message [1] != "") {
						instance.sendData (kinectID + "" + id + message [1]);
					}
			}
		}

		private string getPosition (Joint joint) {
			// dividing as we need an normalized result
			Joint shoulderL = body.Joints [JointType.ShoulderLeft];
			Joint shoulderR = body.Joints [JointType.ShoulderRight];
			float b = shoulderL.Position.X - shoulderR.Position.X;
			b = b * 3;
			Joint head = body.Joints [JointType.Head];
			float h = 0.8; // difference between highest and lowest handposition
			float x = ((joint.Position.X - head.Position.X) / b) + 0.5;
			float y = ((joint.Position.Y - head.Position.Y) / h);
			float z = head.Position.Z - joint.Position.Z;

			if (x > 1) {
				x = 1;
			} else if (x < 0) {
				x = 0;
			}
			if (y > 1) {
				y = 1;
			} else if (y < 0) {
				y = 0;
			}
			if (z > 1) {
				z = 1;
			} else if (z < 0) {
				z = 0;
			}
			string xPos = x + "";
			xPos = xPos.Replace (",", ".");

			string yPos = y + "";
			yPos = yPos.Replace (",", ".");

			string zPos = z + "";
			zPos = zPos.Replace (",", ".");

			string pos = xPos + ";" + yPos + ";" + zPos;
			return pos;
		}

		public void resetHandStates () {
			leftHandState = HandState.NotTracked;
			rightHandState = HandState.NotTracked;
		}
	}




}

