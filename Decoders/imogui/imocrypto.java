/**
 * "Encrypt" class from the imogui Android malware,
 *         used to decrypt the aes encrypted strings
 *         sent and received from C&Cs
 *
 * @author Tim "diff" Strazzere
 *         <diff@lookout.com>
 *         <strazz@gmail.com>
 */
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import org.apache.commons.codec.binary.Base64;

public class imocrypto {
    public static void main(String[] args) {

        if (args.length < 2) {
            System.err.println("Usage: imocrypto e[ncrypt]/d[ecrypt] <data>");
            return;
        }

        if (args[0].toLowerCase().startsWith("e")) {
            System.out.println(encrypt(args[1]));
        } else if (args[0].toLowerCase().startsWith("d")) {
            System.out.println(desEncrypt(args[1]));
        } else {
            System.err.println("Usage: imocrypto e[ncrypt]/d[ecrypt] <data>");
            return;
        }
    }

    // Take a minute to let it sink in... "base64", "desEncrypt", but it's decrypting and using AES...
    // public static java.lang.String com.android.base64.Encryption.desEncrypt(java.lang.String data)
    public static String desEncrypt(String data) {
        try {
            byte[] encrypted = Base64.decodeBase64(data);
            Cipher cipher = Cipher.getInstance("AES/CBC/NoPadding");
            SecretKeySpec keySpec = new SecretKeySpec("1234567812345678".getBytes(), "AES");
            IvParameterSpec ivParameterSpec = new IvParameterSpec("1234567812345678".getBytes());
            cipher.init(Cipher.DECRYPT_MODE, keySpec, ivParameterSpec);
            byte[] original = cipher.doFinal(encrypted);

            // Sloppy way to trip off excess data added for block ciphering
            int a = 0;
            for (int i = original.length - 1; i >= 0; i--) {
                if (original[i] == 0x00) {
                    a++;
                }
            }

            byte[] ye = new byte[original.length - a];

            System.arraycopy(original, 0, ye, 0, ye.length);

            return new String(ye, "UTF-8");
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }

    public static String encrypt(String data) {
        try {
            // Use a million variables because they are insane
            Cipher cipher = Cipher.getInstance("AES/CBC/NoPadding");
            int blockSize = cipher.getBlockSize();
            byte[] dataBytes = data.getBytes();
            int plaintextLength = dataBytes.length;
            // Increase the size to fit blocksize o_O
            if ((plaintextLength % blockSize) != 0) {
                plaintextLength += blockSize - (plaintextLength % blockSize);
            }
            // Create a new array and copy the junk over (this ensures the remaining extra blocks are 0x00
            byte[] plaintext = new byte[plaintextLength];
            System.arraycopy(dataBytes, 0, plaintext, 0, dataBytes.length);
            // Crypto initialization w/ super secret keys/ivs
            SecretKeySpec keySpec = new SecretKeySpec("1234567812345678".getBytes(), "AES");
            IvParameterSpec ivParameterSpec = new IvParameterSpec("1234567812345678".getBytes());

            cipher.init(Cipher.ENCRYPT_MODE, keySpec, ivParameterSpec);
            byte[] encrypted = cipher.doFinal(plaintext);

            return Base64.encodeBase64String(encrypted);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return null;
    }
}
