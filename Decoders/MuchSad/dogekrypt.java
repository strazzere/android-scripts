/**
 * "Krypt" class from the CoinKrypt.A/B (MuchSad.A) Android malware
 * 		used to decrypt the simply obfuscated strings
 * 		in the Main class. Most used for the tracker/
 * 		mining args
 *
 *              Strings / Code reversed from
 *              SHA1: bc27f10178e2bfae277a5b97f1730da5822e4543
 *                    cc8c9ea51a2bdefb4ce9b866eec73a02571bc344
 * 
 * @author Tim "diff" Strazzere
 * 	   <diff@lookout.com>
 * 	   <strazz@gmail.com>
 */
public class dogekrypt {

	public static void main(String[] args) {
	    String[] encrypted_sample1 = {
		"uggc://cbbyfnghea.serr-u.arg/cbby.cuc?c=qngn",
		"uggc://cbbyfnghea.serr-u.arg/hcqngr.cuc?c=qngn",
		"/yvopchzvare.fb --nytb=fpelcg -b uggc://sybj.ybtvagb.zr:9555 -B Q7A6H92Ncdju1NzO4ElMKfIAXUfYDuTYeN:k -e 20 -g 1 -O -d",
		"/yvopchzvare.fb --nytb=fpelcg -b uggc://sybj.ybtvagb.zr:9555 -B Q7A6H92Ncdju1NzO4ElMKfIAXUfYDuTYeN:k -e 20 -g 1 -O -d;",
		"/yvopchzvareARBA.fb --nytb=fpelcg -b uggc://sybj.ybtvagb.zr:9555 -B Q7A6H92Ncdju1NzO4ElMKfIAXUfYDuTYeN:k -e 20 -g 1 -O -d",
		"/yvopchzvareARBA.fb --nytb=fpelcg -b uggc://sybj.ybtvagb.zr:9555 -B Q7A6H92Ncdju1NzO4ElMKfIAXUfYDuTYeN:k -e 20 -g 1 -O -d;",
		"uggc://cbbyfnghea.serr-u.arg/ertvfgre.cuc?vq="
	    };

	    String[] encrypted_sample2 = {
		"/FreivprCebivqre --hey=uggc://91.234.105.69:9327 --hfrecnff=YoULkLThLHRReqcx9L63cvW1N4dW3gAtw1:k --guernqf=1 --ergevrf=5;",
		"/FreivprCebivqre --hey=uggc://91.234.105.69:9327 --hfrecnff=YoULkLThLHRReqcx9L63cvW1N4dW3gAtw1:k --guernqf=1 --ergevrf=5",
		"fbheaq.ab-vc.ovm",
		"uggc://sybjfhes.btfcl.arg/zvare.cuc"
	    };

	    for( String crypted : encrypted_sample1)
		System.out.println(doConvert(crypted));

	    for( String crypted : encrypted_sample2)
		System.out.println(doConvert(crypted));
	}
	
	private static byte abyte;
	
	/**
	 * Black magic; this crypto is insanity
	 * 
	 * TODO: Hire this author for my next project
	 */
	public static String doConvert(String in) {
		StringBuffer tempReturn = new StringBuffer();

		for(int i = 0; i < in.length(); i++) {
			abyte = (byte) in.charAt(i);
			int cap = abyte & 0x20;
			abyte &= (cap ^ -1);
			
			// Is not an alpha capital char?
			if(abyte >= 0x41 && abyte <= 0x5A) {
				abyte += -0x41;
				abyte += 0xD;
				abyte %= 0x1A;
				abyte += 0x41;
			}
			abyte = (byte) (cap | abyte);
			tempReturn.append((char) abyte);
		}

		return tempReturn.toString();
	}
}
