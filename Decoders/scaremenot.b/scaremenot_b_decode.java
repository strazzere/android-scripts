/**
 * "Decode" class from the ScareMeNot.b Android malware,
 *     used for decoding the ransomwares C2 which is often
 *     parse of a string array in the resources file
 *
 * @author Tim "diff" Strazzere
 *         <diff@lookout.com>
 *         <strazz@gmail.com>
 */

import java.io.UnsupportedEncodingException;
import org.apache.commons.codec.binary.Base64;

public class scaremenot_b_decode {

    public static void main(String[] args) {
        try {
            if (args.length < 1) {
                System.err.print("Usage: decode <encoded value[+]>");
                return;
            }
            for (String arg : args) {
                System.out.println(arg + " -> " + decode(arg));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Silly modification to normal base64 decoding
    public static String decode(String data) throws UnsupportedEncodingException {
        StringBuffer buffer = new StringBuffer(data.length());

        for (int i = 0; i < (data.length() / 2); i++) {
            buffer.append(data.charAt((i * 2) + 1));
            buffer.append(data.charAt(i * 2));
        }

        return new String(Base64.decodeBase64(buffer.toString()), "UTF-8");
    }
}
