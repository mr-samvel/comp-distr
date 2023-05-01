import java.lang.SecurityManager;
import java.rmi.Naming;

public class Server {
    public Server() {  
		if(System.getSecurityManager() == null) {
		     System.setSecurityManager(new SecurityManager());
		}
		try {
	        //System.setProperty("java.rmi.server.hostname", "127.0.0.1");
	        //Naming.rebind("rmi://127.0.0.1/Cinema", new Cinema());
	        Naming.rebind("Cinema", new Cinema());
	    }
	    catch(Exception e) {
	        System.out.println("Nao registrou o objeto: " + e);
        }
	}
	
	public static void main(String[] args) {
		new Server();
	}
}
