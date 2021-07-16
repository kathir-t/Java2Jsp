<%@page import="com.your.name.some.other.thing"%>
<%@page import="com.your.name.some.other.thing"%>
<%@page import="com.your.name.some.other.thing"%>



<%

        int times = someLameMethod()

        for (int i=0; i<times; i++) {
            out.print(name);
        }
    
%>


<%!

    public static final String name = "John Doe";

    // (2) the method should be having this same signature
    



    // (3) This is where the rest of the methods should come
    private static int someLameMethod() {
        int times = 1;
        times += 1;
        return times;
    }

%>