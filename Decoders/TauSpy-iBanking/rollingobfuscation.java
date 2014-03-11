/**
 * "MCrypt" class from the iBanking/TauSpy Android malware,
 *         used to decrypt the simply obfuscated strings
 *         in the Main class.
 *
 * @author Tim "diff" Strazzere
 *         <diff@lookout.com>
 *         <strazz@gmail.com>
 */
public class rollingobfuscation {

    // the first argument should be the rolling modifier to start with
    public static void main(String[] args) {
	if(args.length < 2) {
	    System.out.println("Error: please provide a modifier value and atleast on string to decrypt!\n");
	    return;
	}

	for(int i = 1; i < args.length; i++) {
	    System.out.println(decode(args[0], hexStringToString(args[i])));
	}
    }
    
    public static String decode(String modifier, String data) {
	data = transform(Long.parseLong(modifier), data);
	
	// Chop off prefix and add +
	if(data.startsWith("011")) {
	    data = "+" + data.substring(3);
	}
	
	return data;
    }
    
    public static String transform(long modifier, String data) {
	StringBuffer transformed = new StringBuffer();

	long current_char;
	for(int i = 0; i < data.length(); i++){ 
	    current_char = (long)data.charAt(i);
	    transformed.append((char)(current_char ^ (modifier >> 8)));
	    modifier += current_char;
	    modifier *= 0xCE6D;
	    modifier += 0x58BF;
	    modifier %= 0x10000;
	}
	
	return transformed.toString();
    }
    
    public static String hexStringToString(String string) {
	StringBuffer output = new StringBuffer();
	char[] chars = string.toCharArray();
	
	for(int i = 0; i < chars.length - 1; i+= 2) {
	    output.append((char)((Character.digit(chars[i], 0x10) * 0x10) + Character.digit(chars[i+1], 0x10)));
	}
	
	return output.toString();
    }
}
