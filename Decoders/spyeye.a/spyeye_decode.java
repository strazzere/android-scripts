/**
 * "Decode" class from the SpyEye.a Android malware
 * 
 * @author Tim "diff" Strazzere
 *          <diff@lookout.com>
 *          <strazz@gmail.com>
 */

public class spyeye_decode {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.print("Usage: decode <encoded value[+]>");
            return;
        }
        for (String arg : args)
            System.out.println(arg + " -> " + cleanData(arg));
    }

    public static String cleanData(String data) {
        String[] removals = { "[", "]", "=", "-", "q", ",", "<", ">", "\'", ";", "%" };

        for (String removal : removals) {
            data = data.replace(removal, "");
        }

        return data;
    }
}