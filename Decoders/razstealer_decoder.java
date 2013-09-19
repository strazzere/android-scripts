
public class razstealer_decoder {

	public static void main(String[] args) {
	        if(args.length < 1)
		        System.out.println("Pass atleast one string to decode!");
		for(String to_decode : args) {
			System.out.println(decoder(to_decode));
		}
	}
	
	public static String decoder(String data_to_decode) {
		StringBuffer output = new StringBuffer();
		String[] splits = data_to_decode.split("_");
		
		for(String data : splits) {
			output.append(String.valueOf((char)(byte)Math.sqrt(Integer.parseInt(data))));
		}
		
		return output.toString();
	}

}
