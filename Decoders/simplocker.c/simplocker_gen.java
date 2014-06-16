/**
 * Extract out the "gen" method and "rand"
 *    functions pulled from Simplocker.c to
 *    do some testing and see what was going on
 *    in comparison to other randomware variants.
 *
 *    Potentially some overlap with other malware.
 *
 * @author Tim "diff" Strazzere
 *         <diff@lookout.com>
 *         <strazz@gmail.com>
 */
import java.util.Random;

public class simplocker_gen {

    public static void main(String[] args) {
	System.out.println(genkey());
    }

    public static int genkey() {
	int j = 1;
	int k = 9;
	for(int i = 0; i < 5; i++) {
	    j *= 0xA;
	    k = (k * 0xA) + 9;
	}

	return rnd(j, k);
    }

    public static int rnd(int i, int j) {
	return (Math.abs(new Random().nextInt()) % (i -j)) + i;
    }
}
