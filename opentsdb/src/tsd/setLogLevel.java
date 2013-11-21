package net.opentsdb.tsd;

import net.opentsdb.core.TSDB;

import org.jboss.netty.channel.Channel;
import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;

import com.stumbleupon.async.Deferred;

final class setLogLevel implements TelnetRpc {
	public Deferred<Object> execute(final TSDB tsdb, final Channel chan,
			final String[] cmd) {

		logs_set(tsdb,cmd, chan);   
		return Deferred.fromResult(null);

	}

	public Deferred<Object> logs_set(final TSDB tsdb, final String[] words, final Channel chan) {
		// LogIterator logmsgs = new LogIterator();
		words[0]=null;
		String logger_name=null;
		final Level level = Level.toLevel(words[1],
				null);
		if (level == null) {
			throw new BadRequestException("Invalid level: "
					+ words[1]);
		}
		final Logger root =
				(Logger) LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME);
		
		final String root_logger = words[2];
		
		if (root_logger.equals("all")) {
			logger_name = Logger.ROOT_LOGGER_NAME;
		} 
		else{
			logger_name = words[2];
		} 
		if (root.getLoggerContext().exists(logger_name) == null) {
			chan.write("Invalid logger: " + logger_name+ ".\n");
			throw new BadRequestException("Invalid logger: " + logger_name);
		}
		final Logger logger = (Logger) LoggerFactory.getLogger(logger_name);
		int nloggers = 0;
		if (logger == root) {  // Update all the loggers.
			for (final Logger l : logger.getLoggerContext().getLoggerList()) {
				l.setLevel(level);
				nloggers++;
			}
		} else {
			logger.setLevel(level);
			nloggers++;
		}
		//query.sendReply("Set the log level to " + level + " on " + nloggers
		//               + " logger" + (nloggers > 1 ? "s" : "") + ".\n");
		
		chan.write("Set the log level to " +level + " on " + nloggers + 
                                   " logger" + (nloggers > 1 ? "s" : "") + ".\n");

		return Deferred.fromResult(null);
	}


}

