using System;
using System.Collections.Generic;
using RabbitMQ.Client;
using System.Text;
using Microsoft.Kinect;
using Microsoft.Kinect.VisualGestureBuilder;
using System.Threading;
using Kinect;

class Send {
	KinectSensor _kinectSensor;
	BodyFrameSource _bodyFrameSource;
	BodyFrameReader _reader;
	Body[] _bodies;
	IModel _channel;
	private ISet<ulong> trackingIds;
	Dictionary<ulong, Person> mapping;
	List<Person> freePersons;
	static Send send;
	ISet<ulong> ids;
	ConnectionFactory factory;
	IConnection connection;


	public Send () {
		mapping = new Dictionary<ulong, Person> ();
		freePersons = new List<Person> ();
		trackingIds = new HashSet<ulong> ();
		ids = new HashSet<ulong> ();
		inizialiseRabbitMQ ();
		inizialiseKinect ();

	}

	public static void Main () {
		send = new Send ();
		for (int i = 0; i < 6; i++) {
			Person p = new Person (i);
			send.freePersons.Add (p);
		}
		ThreadStart childref = new ThreadStart (send.CallToChildThread);
		Thread childThread = new Thread (childref);
		childThread.Start ();
	}

	public void CallToChildThread () {
		Console.WriteLine ("Enter 'end' to stop");
		string input = "";
		while (input != "end") {
			input = Console.ReadLine ();
		}
		_kinectSensor.Close ();
		_channel.Abort ();
		connection.Close ();
	}

	public static Send getInstance () {
		if (send == null) {
			Console.WriteLine ("there is no instance");
		}
		return send;
	}

	public void sendData (string message) {
		// send data
		var body = Encoding.UTF8.GetBytes (message);

		_channel.BasicPublish (exchange: "",
			routingKey: "hello",
			basicProperties: null,
			body: body);
		//Console.WriteLine (" [x] Sent {0}", message);
	}

	private void inizialiseRabbitMQ () {
		Console.WriteLine ("Inizialising RabbitMQ"); // TODO 
		// Rabbit MQ Connection
		factory = new ConnectionFactory () { HostName = "localhost" };
		connection = factory.CreateConnection ();
		_channel = connection.CreateModel ();
		_channel.QueueDeclare (queue: "hello",
			durable: false,
			exclusive: false,
			autoDelete: false,
			arguments: null);
		
		Console.WriteLine ("Done Inizialising"); //TODO
	}

	private void inizialiseKinect () {
		// Kinect sensor initialization
		while (_kinectSensor == null || !_kinectSensor.IsAvailable) {

			_kinectSensor = KinectSensor.GetDefault ();

			if (_kinectSensor != null) {
				_kinectSensor.Open ();
			}
		}
		Console.WriteLine ("Kinect available");
		_bodyFrameSource = _kinectSensor.BodyFrameSource;
		_reader = _bodyFrameSource.OpenReader ();

		if (_reader != null) {
			_reader.FrameArrived += _reader_FrameArrived;
		}
	}

	private void _reader_FrameArrived (object sender, BodyFrameArrivedEventArgs e) {
		bool dataReceived = false;
		using (BodyFrame bodyFrame = e.FrameReference.AcquireFrame ()) {
			if (bodyFrame != null) {
				if (_bodies == null) {
					_bodies = new Body[bodyFrame.BodyCount];
				}
				bodyFrame.GetAndRefreshBodyData (_bodies);
				dataReceived = true;
			}
		}

		if (dataReceived) {
			ulong trackingId;
			Person p;
			ids.Clear ();
			foreach (Body body in _bodies) {
				if (body != null) {
					if (body.IsTracked) {
						trackingId = body.TrackingId;
						ids.Add (trackingId);
						if (mapping.ContainsKey (trackingId)) {
							p = mapping [trackingId];
						} else {
							p = freePersons [0];
							freePersons.Remove (p);
							mapping [trackingId] = p;
						}
						p.act (body);
					}
				}
			}
			foreach (ulong i in trackingIds) {
				if (!ids.Contains (i)) {
					p = mapping [i];
					p.resetHandStates ();
					freePersons.Add (p);
					trackingIds.Remove (i);
				}
			}
		}
	}


}
