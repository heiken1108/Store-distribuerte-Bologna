# Lab 5 - Kafka

Hands on lab no. 5 in Distributed Software Systems at UNIBO.

## The exercise

1. Set up a Kafka Cluster:
    1. Install and configure Apache Kafka on your local machine or a cloud-based server.
    2. Start a Kafka broker (single-node cluster) with the default configuration.
2. Create a Topic:
    1. Using the Kafka command-line tools (kafka-topics.sh), create a new topic named "testtopic" with a single partition and replication factor of 1.
3. Implement a Kafka Producer:
    1. Write a Python or Java program to create a Kafka producer.
    2. The producer should send a series of messages to the "test-topic" at regular intervals (e.g., every second).
    3. The messages can be simple strings or JSON objects.
4. Implement a Kafka Consumer:
    1. Write a Python or Java program to create a Kafka consumer.
    2. The consumer should subscribe to the "test-topic" and continuously consume msgs.
    3. Print each received message to the console.

## The solution

### Setting up the Kafka cluster

We chose to set up the Kafka environment using the Official JVM Based Docker image. Here is the method from the [Apache Kafka quickstart guide](https://kafka.apache.org/quickstart):

Get the Docker image:

```bash
docker pull apache/kafka:3.8.0
```

Start the Kafka Docker container (this is with port-forwarding so we can access the container using regular ports):

```bash
docker run -d -p 9092:9092 --name broker apache/kafka:3.8.0
```

### Creating a topic

From the documentation of the Official Docker image on [Docker Hub](https://hub.docker.com/r/apache/kafka). Firstly, open a commandline in the running Docker container:

```bash
docker exec --workdir /opt/kafka/bin/ -it broker sh
```

Then, use the built-in `kafka-topics.sh` program to create a topic while in the container:

```bash
./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic
```

### Creating a Kafka Producer

First, we initiated an empty multi module Maven project and added two modules. Then we added the `kafka-clients` dependency and the `exec` plugin to both modules. `kafka-clients` gives us access to the Kafka Producer and Consumer APIs, making us able to publish events to topics and subscribe to topics. 

The constructor of the program class sets up the producer client with the correct configuration. Then we define a method to produce output. This method simply sends the event to the determined topic.

```java
public void produce(String key, String value) {
  producer.send(new ProducerRecord<>(TOPIC, key, value));
}
```

Then we have a run method for the program which reads a file and sends each line as an event to the topic.

```java
public void run() {
  InputStream is = this.getClass().getResourceAsStream("/beemovie.txt");
  try (Scanner sc = new Scanner(is, "utf-8")) {
    while (sc.hasNextLine()) {
      String val = sc.nextLine();
      // Publish the record to the Kafka topic
      this.produce("bee-movie", val);
      System.out.println("Published: " + val);
      // Wait for a random interval between 5 to 10 seconds
      int sleepTime = 5 + ThreadLocalRandom.current().nextInt(6);
      TimeUnit.SECONDS.sleep(sleepTime);
    }
  } catch (InterruptedException e) {
    e.printStackTrace();
  } finally {
    producer.close();
  }
}
```

### Creating the Kafka Consumer

We now moved to the consumer module. The methodology is almost the same, but now for consumption of events.

The constructor of the ConsumerProgram class makes a correctly configured KafkaConsumer and assigns it to the instance. Then we have the run method which subscribes to the topic and then infinitely polls the topic every scond for new records. If new records are retrieved, their value will be printed.

```java
public void run() {
  // Subscribe to the Kafka topic
  try {
    consumer.subscribe(Collections.singletonList(TOPIC));
    while (true) {
      // Poll for new records
      try {
        consumer.poll(Duration.ofMillis(1000)).forEach(record -> {
          System.out.println("Received: " + record.value());
        });
      } catch (Exception e) {
        e.printStackTrace();
      }
    }
  } catch (Exception e) {
    e.printStackTrace();
  } finally {
    consumer.close();
  }
}
```

## Running the solution

Make sure that the Docker container with the Kafka broker is running. To enter the Maven project and install it run:

```bash
cd kafka-exercise
mvn install
```

Then you can start the producer by running

```bash
cd producer
mvn exec:java
```

Start a separate terminal that can run the consumer. Make sure that you are in the directory `kafka-exercise/consumer` before running the command below to start the consumer.

```bash
mvn exec:java
```

Now you should see the Bee Movie script being published and received at irregular intervals between 5-10 seconds.
