package dss.kafka;

import java.io.InputStream;
import java.util.Properties;
import java.util.Scanner;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

/**
 * The ProducerProgram class is responsible for producing messages to a Kafka
 * topic.
 * 
 * <p>
 * It initializes a Kafka producer with the necessary properties and provides
 * methods
 * to send messages to a specified topic. The main functionality includes
 * reading lines
 * from a file and publishing each line as a record to the Kafka topic.
 * </p>
 * 
 * <p>
 * The class includes the following methods:
 * <ul>
 * <li>{@link #ProducerProgram()}: Initializes the Kafka producer with specified
 * properties.</li>
 * <li>{@link #produce(String, String)}: Sends a message to the Kafka
 * topic.</li>
 * <li>{@link #run()}: Reads lines from a file and publishes each line to the
 * Kafka topic.</li>
 * </ul>
 * </p>
 * 
 * <p>
 * The main method creates an instance of the ProducerProgram and runs it.
 * </p>
 * 
 * <p>
 * Example usage:
 * 
 * <pre>
 * {@code
 * ProducerProgram producerProgram = new ProducerProgram();
 * producerProgram.run();
 * }
 * </pre>
 * </p>
 * 
 * <p>
 * Note: Ensure that Kafka is running and accessible at the specified bootstrap
 * servers.
 * </p>
 *
 * @see org.apache.kafka.clients.producer.KafkaProducer
 * @see org.apache.kafka.clients.producer.ProducerRecord
 */
public class ProducerProgram {

  private Producer<String, String> producer;
  public static final String TOPIC = "test-topic";

  /**
   * Initializes a new instance of the ProducerProgram class.
   * 
   * This constructor sets up the necessary properties for the Kafka producer,
   * including the bootstrap servers, linger time, key serializer, and value
   * serializer.
   * It then creates a new KafkaProducer instance with these properties.
   */
  public ProducerProgram() {
    Properties props = new Properties();
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

    // Create a new KafkaProducer
    producer = new KafkaProducer<>(props);
  }

  /**
   * Sends a message to the Kafka topic.
   *
   * @param key   the key of the message
   * @param value the value of the message
   */
  public void produce(String key, String value) {
    producer.send(new ProducerRecord<>(TOPIC, key, value));
  }

  /**
   * Runs the producer program that reads lines from the "beemovie.txt" file
   * and publishes each line as a record to the Kafka topic "bee-movie".
   * 
   * <p>
   * The method performs the following steps:
   * <ul>
   * <li>Opens the "beemovie.txt" file as an InputStream.</li>
   * <li>Uses a Scanner to read the file line by line.</li>
   * <li>Publishes each line to the Kafka topic "bee-movie".</li>
   * <li>Prints the published line to the console.</li>
   * <li>Waits for a random interval between 5 to 10 seconds before reading the
   * next line.</li>
   * <li>Handles InterruptedException if the thread is interrupted during
   * sleep.</li>
   * <li>Closes the Kafka producer in the finally block to ensure resources are
   * released.</li>
   * </ul>
   *
   * @throws InterruptedException if the thread is interrupted while sleeping.
   */
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

  public static void main(String[] args) {
    ProducerProgram producerProgram = new ProducerProgram();
    producerProgram.run();
  }

}