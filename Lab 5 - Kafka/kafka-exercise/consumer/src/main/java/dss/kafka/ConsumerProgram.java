package dss.kafka;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

/**
 * The ConsumerProgram class is responsible for consuming messages from a Kafka
 * topic.
 * 
 * <p>
 * This class sets up a Kafka consumer with the following properties:
 * <ul>
 * <li>Bootstrap servers are set to "localhost:9092".</li>
 * <li>Key deserializer class is set to StringDeserializer.</li>
 * <li>Value deserializer class is set to StringDeserializer.</li>
 * <li>Consumer group ID is set to "test-group".</li>
 * </ul>
 * 
 * <p>
 * The class provides a method to run the consumer, which subscribes to a
 * specified Kafka topic
 * and continuously polls for new records. For each received record, it prints
 * the record's value
 * to the standard output. The consumer is properly closed to ensure resource
 * cleanup.
 * 
 * <p>
 * Usage example:
 * 
 * <pre>
 * {@code
 * public static void main(String[] args) {
 *   ConsumerProgram consumerProgram = new ConsumerProgram();
 *   consumerProgram.run();
 * }
 * }
 * </pre>
 * 
 * <p>
 * Note: This example assumes that a Kafka broker is running on localhost:9092
 * and that the
 * topic "test-topic" exists.
 * 
 * <p>
 * Exceptions that may occur during subscription and polling are caught and
 * their stack traces
 * are printed.
 *
 * @see org.apache.kafka.clients.consumer.Consumer
 * @see org.apache.kafka.clients.consumer.KafkaConsumer
 * @see org.apache.kafka.clients.consumer.ConsumerConfig
 * @see org.apache.kafka.common.serialization.StringDeserializer
 */
public class ConsumerProgram {

  private Consumer<String, String> consumer;
  public static final String TOPIC = "test-topic";

  /**
   * Initializes a new instance of the ConsumerProgram class.
   * 
   * This constructor sets up the Kafka consumer with the necessary properties:
   * - Bootstrap servers are set to "localhost:9092".
   * - Key deserializer class is set to StringDeserializer.
   * - Value deserializer class is set to StringDeserializer.
   * - Consumer group ID is set to "test-group".
   * 
   * The KafkaConsumer instance is created with the specified properties.
   */
  public ConsumerProgram() {
    Properties props = new Properties();
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
        StringDeserializer.class.getName());
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
        StringDeserializer.class.getName());
    props.put(ConsumerConfig.GROUP_ID_CONFIG, "test-group");
    consumer = new KafkaConsumer<>(props);
  }

  /**
   * Runs the Kafka consumer program.
   * 
   * This method subscribes to the specified Kafka topic and continuously polls
   * for new records.
   * For each received record, it prints the record's value to the standard
   * output.
   * 
   * The method handles exceptions that may occur during subscription and polling,
   * printing the stack trace of any caught exceptions.
   * 
   * The consumer is closed in the finally block to ensure proper resource
   * cleanup.
   */
  public void run() {
    // Subscribe to the Kafka topic
    try {
      consumer.subscribe(Collections.singletonList(TOPIC));
      while (true) {
        // Poll for new records
        try {
          consumer.poll(Duration.ofMillis(100)).forEach(record -> {
            System.out.println("Received: " + record.value());
          });
        } catch (Exception e) {
          // TODO Auto-generated catch block
          e.printStackTrace();
        }
      }
    } catch (Exception e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    } finally {
      consumer.close();
    }
  }

  public static void main(String[] args) {
    ConsumerProgram consumerProgram = new ConsumerProgram();
    consumerProgram.run();
  }
}