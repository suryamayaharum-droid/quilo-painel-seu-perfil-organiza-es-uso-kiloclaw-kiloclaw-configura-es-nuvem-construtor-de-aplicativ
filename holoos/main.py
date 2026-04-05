"""
HoloOS Main Entry Point
=======================
Initialize and run the HoloOS system.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("holoos")


def main():
    logger.info("=" * 60)
    logger.info("HoloOS v0.7.0 - Starting System...")
    logger.info("=" * 60)
    
    try:
        from holoos import (
            get_coordinator,
            get_ethical_core,
            get_super_intelligence,
            get_memory,
            get_planner,
            get_communication_hub,
            get_tool_executor,
            get_gateway,
            get_database,
            get_monitoring,
            get_plugin_manager,
            get_config,
            get_security_kernel,
            get_soul,
            get_assembly,
        )
        
        logger.info("Initializing modules...")
        
        coordinator = get_coordinator()
        logger.info("✓ Pipeline Coordinator")
        
        ethical = get_ethical_core()
        logger.info("✓ Ethical Core")
        
        ai = get_super_intelligence()
        logger.info("✓ Super Intelligence (17 models)")
        
        memory = get_memory()
        logger.info("✓ Unified Memory")
        
        planner = get_planner()
        logger.info("✓ Planner & Reasoning")
        
        comm = get_communication_hub()
        logger.info("✓ Communication Hub")
        
        tools = get_tool_executor()
        logger.info("✓ Tool Executor (9 tools)")
        
        gateway = get_gateway()
        logger.info("✓ API Gateway")
        
        db = get_database()
        logger.info("✓ Database Manager")
        
        monitor = get_monitoring()
        logger.info("✓ Monitoring System")
        
        plugins = get_plugin_manager()
        logger.info("✓ Plugin Manager")
        
        config = get_config()
        logger.info("✓ Config Manager")
        
        security = get_security_kernel()
        logger.info("✓ Security Kernel")
        
        soul = get_soul()
        logger.info("✓ Soul/Identity")
        
        assembly = get_assembly()
        logger.info("✓ Governance Assembly")
        
        logger.info("=" * 60)
        logger.info("HoloOS v0.7.0 - All Systems Online!")
        logger.info("=" * 60)
        
        logger.info("\nSystem Status:")
        logger.info(f"  - AI Models: {len(ai.get_available_models())}")
        logger.info(f"  - Memory: {memory.get_status()}")
        logger.info(f"  - Tools: {len(tools.registry.list_tools())}")
        logger.info(f"  - Gateway Routes: {gateway.get_status()['routes']}")
        logger.info(f"  - Database: {db.get_stats()}")
        logger.info(f"  - Security Level: {security.get_status()['security_level']}")
        
        print("\n" + "=" * 60)
        print("HoloOS is running! Press Ctrl+C to stop.")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"Error starting system: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()