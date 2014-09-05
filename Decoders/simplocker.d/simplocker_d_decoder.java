/**
 * "Decode" class from the simplocker.d Android malware,
 *      lazily will try the two different keys I've seen
 *      in the wild being used to try to decode the config.
 *
 * @author Tim "diff" Strazzere
 *         <diff@lookout.com>
 *         <strazz@gmail.com>
 */
import java.net.URLDecoder;

public class simplocker_d_decoder {

    public static void main(String[] args) {

        if (args.length < 1) {
            System.err.println("Usages: decode <url encoded config strings [+]>");
            return;
        }

        for (String arg : args) {
            String[] config = decode(arg);

            if (config == null) {
                System.err.println("Error: likely an unknown xor key being used!");
                return;
            }

            if (config.length != 5) {
                System.err.println("Warning: odd returned length of config!");
            }

            System.out.println("C2: " + config[0]);
            System.out.println("Unused: " + config[1]);
            System.out.println("Client Number: " + config[2]);
            System.out.println("AES Encryption Key: " + config[3]);
            System.out.println("Extensions to encrypt: " + config[4]);
            System.out.println("");
        }
    }

    public static String[] decode(String data) {
        String[] keys = { "chihanin", "ebcncjejane" };
        for (String key : keys) {
            String[] attempt = decode(data, key);
            if (attempt.length == 5) {
                return attempt;
            }
        }

        return null;
    }

    @SuppressWarnings("deprecation")
    public static String[] decode(String data, String xor_key) {

        data = URLDecoder.decode(data);

        StringBuffer buffer = new StringBuffer(data);
        int x = 0;

        for (int i = 0; i < data.length(); i++) {
            if (x >= xor_key.length()) {
                x = 0;
            }
            buffer.setCharAt(i, (char) (data.charAt(i) ^ xor_key.charAt(x)));
            x++;
        }

        return buffer.toString().split(",");
    }
}
