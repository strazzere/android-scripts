/**
 * "MCrypt" class from the iBanking/TauSpy Android malware,
 *         used to decrypt the aes encrypted strings
 *         in the Main class.
 *
 * @author Tim "diff" Strazzere
 *         <diff@lookout.com>
 *         <strazz@gmail.com>
 */

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;


public class mcrypt {

    public static byte[] iv;
    public static SecretKey key;
    public static Cipher cipher;

    public static void main(String[] args) {
	if(args.length < 3) {
	    System.out.println("Error; must include three args, ivString, keyString and text to decrypt");
	    return;
	}
	initialize(args[0], args[1]);
	for(int i = 2; i < args.length; i++) {
	    System.out.println(new String(decrypt(args[i])));
	}
    }

    public static byte[] hexStringToByteArray(String s) {
	int len = s.length();
	byte[] data = new byte[len / 2];
	for (int i = 0; i < len; i += 2) {
	    data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
				  + Character.digit(s.charAt(i+1), 16));
	}
	return data;
    }
    
    public static void initialize(String ivString, String keyString) {
        iv = ivString.getBytes();
        byte[] keyBytes = keyString.getBytes();
        
        key = new SecretKeySpec(keyBytes, "AES");
	try {
	    cipher = Cipher.getInstance("AES/CBC/NOPADDING");
	} catch (Exception e) {
	    e.printStackTrace();
	}
    }
    
    public static byte[] decrypt(String input) {
	if(input.length() > 0){
	    try {
		cipher.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));
		byte[] decrypted = cipher.doFinal(hexStringToByteArray(input));
		// Strip padding (weird way to do it, but same way malware does)
		int trim = 0;
		for(int i = decrypted.length - 1; i >= 0 ; i--) {
		    if(decrypted[i] == 0) {
			trim++;
		    }
		}
		byte[] trimmed = new byte[decrypted.length - trim];
		System.arraycopy(decrypted, 0, trimmed, 0, decrypted.length - trim);
		return trimmed;
	    } catch (Exception e) {
		e.printStackTrace();
	    }
	}
        return null;
    }
}
