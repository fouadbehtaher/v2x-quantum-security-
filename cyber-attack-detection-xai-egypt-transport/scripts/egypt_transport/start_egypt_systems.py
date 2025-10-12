#!/usr/bin/env python3
"""
سكريبت تشغيل أنظمة النقل المصرية مع الأمن السيبراني
Startup Script for Egyptian Transport Systems with Cybersecurity
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# إضافة المسارات
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

async def main():
    """الدالة الرئيسية لتشغيل الأنظمة المصرية"""
    print("🚗 بدء تشغيل أنظمة النقل الذكي في مصر مع الأمن السيبراني...")
    
    try:
        # 1. تشغيل نظام القاهرة
        from egypt_transport.transport_systems.cairo_smart_traffic import CairoSmartTrafficSystem
        cairo_system = CairoSmartTrafficSystem()
        print("✅ نظام النقل الذكي في القاهرة - جاهز")
        
        # 2. تشغيل أنظمة الدفع
        from egypt_transport.payment_systems.electronic_payment import EgyptPaymentSystems
        payment_systems = EgyptPaymentSystems({})
        print("✅ أنظمة الدفع الإلكتروني - جاهزة")
        
        # 3. التكامل مع وزارة النقل
        from egypt_transport.government_integration.ministry_transport_api import MinistryTransportIntegration
        ministry_integration = MinistryTransportIntegration({})
        print("✅ التكامل مع وزارة النقل - جاهز")
        
        # 4. بدء المراقبة
        print("\n🔍 بدء مراقبة أنظمة النقل...")
        await start_monitoring(cairo_system, payment_systems, ministry_integration)
        
    except Exception as e:
        print(f"❌ فشل تشغيل الأنظمة: {e}")
        sys.exit(1)

async def start_monitoring(cairo_system, payment_systems, ministry_integration):
    """بدء مراقبة الأنظمة"""
    while True:
        try:
            # مراقبة أنظمة القاهرة
            cairo_status = await cairo_system.monitor_traffic_systems()
            
            # مراقبة أنظمة الدفع
            payment_metrics = await payment_systems.get_transaction_metrics()
            
            # التحقق من الامتثال
            compliance_status = await ministry_integration.validate_system_compliance("cairo_traffic")
            
            # عرض النتائج
            print(f"\n📊 تحديث المراقبة - {datetime.now()}")
            print(f"   • حركة المرور: {cairo_status['system_status']['traffic_management']['traffic_flow']}")
            print(f"   • المعاملات: {payment_metrics['success_rate']:.1%} نجاح")
            print(f"   • الامتثال: {compliance_status['compliance_status']}")
            
            # التحقق من الإنذارات الأمنية
            if cairo_status['security_alerts']:
                print(f"   ⚠️  إنذارات أمنية: {len(cairo_status['security_alerts'])}")
                for alert in cairo_status['security_alerts']:
                    print(f"     - {alert['type']}: {alert['description']}")
            
            # الانتظار قبل التحديث التالي
            await asyncio.sleep(60)  # كل دقيقة
            
        except KeyboardInterrupt:
            print("\n🛑 إيقاف المراقبة...")
            break
        except Exception as e:
            print(f"❌ خطأ في المراقبة: {e}")
            await asyncio.sleep(30)  # الانتظار قبل إعادة المحاولة

if __name__ == "__main__":
    # تشغيل النظام
    asyncio.run(main())
